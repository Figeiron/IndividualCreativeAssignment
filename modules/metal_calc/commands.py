from core.command import Command
from core.parameter import Parameter, RangeValidator, IndexParameter
from abc import ABC


class CalculateMetalCommand(Command, ABC):
    @classmethod
    def get_params(cls, service):
        materials_count = service.get_materials_count()
        return super().get_params(service) + [
            IndexParameter("material_index", "Матеріал", f"від 1 до {materials_count}", int,
                           validators=[RangeValidator(1, materials_count)]),
        ]

    def __init__(self, service, material_index):
        self.service = service
        self.material_index = material_index


class CalculateMetalRoundCommand(CalculateMetalCommand, ABC):
    @classmethod
    def get_params(cls, service):
        return super().get_params(service) + [
            Parameter("diameter", "Діаметр", "Діаметр труби в мм", float, validators=[RangeValidator(min_val=1)]),
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
            Parameter("length", "Довжина", "Довжина труби в мм", float, validators=[RangeValidator(min_val=1)])
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
            Parameter("angle", "Кут", "Кут коліна в градусах", float, validators=[RangeValidator(0, 360)]),
            Parameter("segments", "Сегменти", "Кількість сегментів", int, validators=[RangeValidator(min_val=1)])
        ]

    def __init__(self, service, material_index, diameter, angle, segments):
        super().__init__(service, material_index, diameter)
        self.angle = angle
        self.segments = segments

    def _execute(self, context):
        return self.service.calculate_elbow_unfolding(self.diameter, self.angle, self.segments, self.material_index)
