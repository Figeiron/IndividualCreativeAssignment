import math
from core.service import Service
from core.response import Response, TextBox, PlotBox, TableBox, TableCell
from modules.metal_calc.commands import *
from modules.metal_calc.providers.materials_provider import MaterialsProvider
from modules.metal_calc.models.products import Pipe, Elbow
from modules.metal_calc.models.materials import MetalMaterial


class MetalCalcService(Service):
    displayed_name = "Калькулятор тонколистового металу"

    DEFAULT_DIAMETERS = (100.0, 125.0, 150.0, 200.0, 250.0, 315.0)

    @classmethod
    def get_default_diameters(cls):
        return list(cls.DEFAULT_DIAMETERS)

    def __init__(self, context):
        super().__init__(context)
        self.materials_provider = MaterialsProvider()
        self.materials = self.materials_provider.thin_metals

        self.register_command(GetMaterialsCommand.name, GetMaterialsCommand)
        self.register_command(CalculatePipeCommand.name, CalculatePipeCommand)
        self.register_command(CalculateElbowCommand.name, CalculateElbowCommand)
        self.register_command(AddMaterial.name, AddMaterial)
        self.register_command(DeleteMaterial.name, DeleteMaterial)
        self.register_command(AirFlowPlot.name, AirFlowPlot)

    def get_materials(self):
        result = "Доступні тонколистові метали (ціна за м2):\n"
        for material in sorted(self.materials, key=lambda x: x.id):
            result += f"{material.id + 1}. {material.name}: {material.price_per_m2} грн/м2\n"
        return Response(boxes=[TextBox(text=result.strip())])

    def get_materials_count(self):
        return len(self.materials)

    def get_materials_mapped(self):
        return [(m.name, m.id) for m in self.materials]

    def get_material_by_id(self, idx):
        for material in self.materials:
            if material.id == idx:
                return material
        else:
            raise IndexError(f"Material with {idx} not defined")

    def add_material(self, name, price_per_m2, salary_per_m2):
        old_materials = self.materials
        new_material = MetalMaterial(
            name=name,
            price_per_m2=price_per_m2,
            salary_per_m2=salary_per_m2,
        )
        new_materials = old_materials + [
            new_material
        ]

        self.materials_provider.save_materials(new_materials)
        self.update_materials()
        return Response(boxes=[TextBox(text="Матеріал успішно додано.")])

    def delete_material(self, material_idx):
        if self.get_materials_count() <= 1:
            raise ValueError("Materials must be >= 1")

        old_materials = self.materials
        new_materials = [m for m in old_materials if m.id != material_idx]

        self.materials_provider.save_materials(new_materials)
        self.update_materials()
        return Response(boxes=[TextBox(text="Матеріал успішно видалено.")])

    def update_materials(self):
        self.materials = self.materials_provider.load_materials()

    def calculate_pipe_unfolding(self, diameter_mm: float, length_mm: float, material_index: int, has_salary: bool):
        material = self.get_material_by_id(material_index)
        pipe = Pipe(diameter_mm=diameter_mm, material=material, length_mm=length_mm, has_salary=has_salary)
        return Response(boxes=[
            TextBox(text="Труба"),
            TableBox([
                TableCell(pos=(0, 0), text="Параметер"),
                TableCell(pos=(1, 0), text="Виріб:"),
                TableCell(pos=(2, 0), text="Розгортка:"),
                TableCell(pos=(3, 0), text="Матеріал:"),
                TableCell(pos=(4, 0), text="Площа:"),
                TableCell(pos=(5, 0), text="Вартість:"),
                TableCell(pos=(0, 1), text="Значення"),
                TableCell(pos=(1, 1), text=f"Труба (Діаметр: {pipe.diameter_mm} мм, Довжина: {pipe.length_mm} мм)"),
                TableCell(pos=(2, 1), text=f"{pipe.get_width_mm():.2f} x {pipe.length_mm} мм"),
                TableCell(pos=(3, 1), text=f"{pipe.material.name}"),
                TableCell(pos=(4, 1), text=f"{pipe.get_area_m2():.3f} м2"),
                TableCell(pos=(5, 1), text=f"{pipe.get_cost():.2f} грн")
            ])
        ])

    def calculate_elbow_unfolding(self, diameter_mm: float, angle_deg: float, segments: int, material_index: int,
                                  has_salary: bool):
        material = self.get_material_by_id(material_index)
        elbow = Elbow(diameter_mm=diameter_mm, material=material, angle_deg=angle_deg, segments=segments,
                      has_salary=has_salary)
        return Response(boxes=[TextBox(text=str(elbow))])

    def calculate_air_flow_plot(self, diameter_mm: float, speed_min: float = 1, speed_max: float = 10):
        step = 0.5
        d = diameter_mm / 1000
        area = math.pi * d ** 2 / 4

        def calc_q(v, a):
            return v * a * 3600

        points = []

        steps_count = int((speed_max - speed_min) / step)

        for i in range(steps_count + 1):
            v = speed_min + i * step
            q = calc_q(v, area)
            points.append((round(v,2), round(q,2)))
        
        test_points = [(x, abs(x**3) ) for x in range(int(speed_min), int(speed_max)+1)]
        return Response(boxes=[
            PlotBox(points),
            TextBox("Точки"),
            TableBox([TableCell((0, x), str(point)) for x, point in enumerate(points)]),
            PlotBox(test_points)])
