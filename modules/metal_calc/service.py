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
        for i, material in enumerate(self.materials):
            result += f"{i + 1}. {material.name}: {material.price_per_m2} грн/м2\n"
        return result.strip()

    def calculate_pipe_unfolding(self, diameter_mm: float, length_mm: float, material_index: int):
        if not (0 <= material_index < len(self.materials)):
            return "Помилка: Невірний індекс матеріалу."

        material = self.materials[material_index]
        pipe = Pipe(diameter_mm=diameter_mm, material=material, length_mm=length_mm)
        return str(pipe)

    def calculate_elbow_unfolding(self, diameter_mm: float, angle_deg: float, segments: int, material_index: int):
        if not (0 <= material_index < len(self.materials)):
            return "Помилка: Невірний індекс матеріалу."

        material = self.materials[material_index]
        elbow = Elbow(diameter_mm=diameter_mm, material=material, angle_deg=angle_deg, segments=segments)
        return str(elbow)
