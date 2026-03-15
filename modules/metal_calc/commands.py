from core.command import Command
from core.parameter import Parameter, RangeValidator, IndexParameter
from abc import ABC, abstractmethod

class CalculateMetalCommand(Command):
    @classmethod
    def get_params(cls, service=None):

        materials_count = len(service.materials)
        return [ 
            IndexParameter("material_index", "Індекс матеріалу", f"від 1 до {materials_count}", int,
                           validators=[RangeValidator(1, materials_count)]),
        ]

class GetMaterialsCommand(Command):
    name = "Довідник матеріалів"
    description = "Показати доступні тонколистові метали"

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_materials()


class CalculatePipeCommand(CalculateMetalCommand):
    name = "Розрахувати трубу"
    description = "Розрахувати розгортку та вартість труби"

    @classmethod
    def get_params(cls, service=None):
        return super().get_params(service) + [
            Parameter("diameter", "Діаметер", "Діаметер труби в мм", float, validators=[RangeValidator(min_val=1)]),
            Parameter("length", "Довжина", "Довжина труби в мм", float, validators=[RangeValidator(min_val=1)])
        ]
    def __init__(self, service, diameter, length, material_index):
        self.service = service
        self.diameter = diameter
        self.length = length
        self.material_index = material_index

    def _execute(self, context):
        return self.service.calculate_pipe_unfolding(self.diameter, self.length, self.material_index)


class CalculateElbowCommand(Command):
    name = "Розрахувати коліно"
    description = "Розрахувати приблизну вартість коліна"

    @classmethod
    def get_params(cls, service=None):
        materials_count = len(service.materials)
        return [
            Parameter("diameter", "Діаметер", "Діаметер труби в мм", float, validators=[RangeValidator(min_val=1)]),
            Parameter("angle", "Кут", "Кут коліна в градусах", float, validators=[RangeValidator(0, 360)]),
            Parameter("segments", "Сегменти", "Кількість сегментів", int, validators=[RangeValidator(min_val=1)]),
            IndexParameter("material_index", "Індекс матеріалу", f"від 1 до {materials_count}", int,
                      validators=[RangeValidator(1, materials_count)])
        ]

    def __init__(self, service, diameter, angle, segments, material_index):
        self.service = service
        self.diameter = diameter
        self.angle = angle
        self.segments = segments
        self.material_index = material_index

    def _execute(self, context):
        return self.service.calculate_elbow_unfolding(self.diameter, self.angle, self.segments, self.material_index)
