from core.service import Service
from modules.metal_calc.commands import *
from modules.metal_calc.models.materials import THIN_METALS
from modules.metal_calc.models.products import Pipe, Elbow


class MetalCalcService(Service):
    displayed_name = "Калькулятор тонколистового металу"

    def __init__(self, context):
        super().__init__(context)
        self.materials = THIN_METALS

        self.register_command(GetMaterialsCommand.name, GetMaterialsCommand)
        self.register_command(CalculatePipeCommand.name, CalculatePipeCommand)
        self.register_command(CalculateElbowCommand.name, CalculateElbowCommand)

    def get_materials(self):
        result = "Доступні тонколистові метали (ціна за м2):\n"
        for material in sorted(self.materials, key=lambda x: x.id):
            result += f"{material.id + 1}. {material.name}: {material.price_per_m2} грн/м2\n"
        return result.strip()

    def get_materials_count(self):
        return len(self.materials)

    def get_material_by_id(self, idx):
        for material in self.materials:
            if material.id == idx:
                return material
        else:
            raise IndexError(f"Material with {idx} not defined")

    def calculate_pipe_unfolding(self, diameter_mm: float, length_mm: float, material_index: int, has_salary: bool):
        material = self.get_material_by_id(material_index)
        pipe = Pipe(diameter_mm=diameter_mm, material=material, length_mm=length_mm, has_salary=has_salary)
        return str(pipe)

    def calculate_elbow_unfolding(self, diameter_mm: float, angle_deg: float, segments: int, material_index: int, has_salary: bool):
        material = self.get_material_by_id(material_index)
        elbow = Elbow(diameter_mm=diameter_mm, material=material, angle_deg=angle_deg, segments=segments, has_salary=has_salary)
        return str(elbow)
