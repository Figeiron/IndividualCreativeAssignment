from core.command import Command
from modules.metal_calc.schemas.parameters import *
from abc import ABC


class CalculateMetalCommand(Command, ABC):
    @classmethod
    def get_params(cls, service):
        materials_count = service.get_materials_count()
        return [
            MATERIAL_IDX.with_range(1, materials_count).build(custom_desc=f"від 1 до {materials_count}")
        ]

    def __init__(self, service, material_index):
        self.service = service
        self.material_index = material_index


class CalculateMetalRoundCommand(CalculateMetalCommand, ABC):
    @classmethod
    def get_params(cls, service):
        return super().get_params(service) + [
            DIAMETER.with_range(min_val=1).build()
        ]

    def __init__(self, service, material_index, diameter):
        super().__init__(service, material_index)
        self.diameter = diameter


class GetMaterialsCommand(Command):
    name = "Довідник матеріалів"
    description = "Показати доступні тонколистові метали"

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_materials()


class CalculatePipeCommand(CalculateMetalRoundCommand):
    name = "Розрахувати трубу"
    description = "Розрахувати розгортку та вартість труби"

    @classmethod
    def get_params(cls, service):
        return super().get_params(service) + [
            LENGTH.with_range(min_val=1).build()
        ]

    def __init__(self, service, material_index, diameter, length):
        super().__init__(service, material_index, diameter)
        self.length = length

    def _execute(self, context):
        return self.service.calculate_pipe_unfolding(self.diameter, self.length, self.material_index)


class CalculateElbowCommand(CalculateMetalRoundCommand):
    name = "Розрахувати коліно"
    description = "Розрахувати приблизну вартість коліна"

    @classmethod
    def get_params(cls, service):
        return super().get_params(service) + [
            ANGLE.with_range(0, 360).build(),
            SEGMENTS.with_range(min_val=1).build()
        ]

    def __init__(self, service, material_index, diameter, angle, segments):
        super().__init__(service, material_index, diameter)
        self.angle = angle
        self.segments = segments

    def _execute(self, context):
        return self.service.calculate_elbow_unfolding(self.diameter, self.angle, self.segments, self.material_index)
