from core.command import Command
from modules.metal_calc.schemas.parameters import *
from abc import ABC


class CalculateMetalCommand(Command, ABC):
    @classmethod
    def get_params(cls, service):
        materials = service.get_materials_mapped()
        return [
            HAS_SALARY.build(),
            MATERIAL_IDX.with_mapped_choices(materials).build()
        ]

    def __init__(self, service, has_salary, material_index):
        self.service = service
        self.has_salary = has_salary
        self.material_index = material_index


class CalculateMetalRoundCommand(CalculateMetalCommand, ABC):
    @classmethod
    def get_params(cls, service):

        return super().get_params(service) + [
            DIAMETER.with_range(min_val=1).build()
        ]

    def __init__(self, service, has_salary, material_index, diameter):
        super().__init__(service, has_salary, material_index)
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

    def __init__(self, service, has_salary, material_index, diameter, length):
        super().__init__(service, has_salary, material_index, diameter)
        self.length = length

    def _execute(self, context):
        return self.service.calculate_pipe_unfolding(self.diameter, self.length, self.material_index, self.has_salary)


class CalculateElbowCommand(CalculateMetalRoundCommand):
    name = "Розрахувати коліно"
    description = "Розрахувати приблизну вартість коліна"

    @classmethod
    def get_params(cls, service):
        return super().get_params(service) + [
            ANGLE.with_range(0, 360).build(),
            SEGMENTS.with_range(min_val=1).build()
        ]

    def __init__(self, service, has_salary, material_index, diameter, angle, segments):
        super().__init__(service, has_salary, material_index, diameter)
        self.angle = angle
        self.segments = segments

    def _execute(self, context):
        return self.service.calculate_elbow_unfolding(self.diameter, self.angle, self.segments, self.material_index, self.has_salary)
