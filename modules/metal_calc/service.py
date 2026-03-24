from core.service import Service
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

    def get_materials(self):
        result = "Доступні тонколистові метали (ціна за м2):\n"
        for material in sorted(self.materials, key=lambda x: x.id):
            result += f"{material.id + 1}. {material.name}: {material.price_per_m2} грн/м2\n"
        return result.strip()

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

    def delete_material(self, material_idx):
        if self.get_materials_count() <= 1:
            raise ValueError("Materials must be >= 1")

        old_materials = self.materials
        new_materials = [m for m in old_materials if m.id != material_idx]

        self.materials_provider.save_materials(new_materials)
        self.update_materials()

    def update_materials(self):
        self.materials = self.materials_provider.load_materials()

    def calculate_pipe_unfolding(self, diameter_mm: float, length_mm: float, material_index: int, has_salary: bool):
        material = self.get_material_by_id(material_index)
        pipe = Pipe(diameter_mm=diameter_mm, material=material, length_mm=length_mm, has_salary=has_salary)
        return str(pipe)

    def calculate_elbow_unfolding(self, diameter_mm: float, angle_deg: float, segments: int, material_index: int,
                                  has_salary: bool):
        material = self.get_material_by_id(material_index)
        elbow = Elbow(diameter_mm=diameter_mm, material=material, angle_deg=angle_deg, segments=segments,
                      has_salary=has_salary)
        return str(elbow)
