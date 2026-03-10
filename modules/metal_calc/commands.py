from core.command import Command


class GetMaterialsCommand(Command):
    name = "Довідник матеріалів"
    description = "Показати доступні тонколистові метали"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_materials()


class CalculatePipeCommand(Command):
    name = "Розрахувати трубу"
    description = "Розрахувати розгортку та вартість труби (діаметр(мм), довжина(мм), індекс_матеріалу)"
    expected_params = ["diameter", "length", "material_index"]

    def __init__(self, service, diameter, length, material_index):
        self.service = service
        self.diameter = float(diameter)
        self.length = float(length)
        self.material_index = int(material_index) - 1

    def _execute(self, context):
        return self.service.calculate_pipe_unfolding(self.diameter, self.length, self.material_index)


class CalculateElbowCommand(Command):
    name = "Розрахувати коліно"
    description = "Розрахувати приблизну вартість коліна (діаметр(мм), кут(градуси), сегментів, індекс_матеріалу)"
    expected_params = ["diameter", "angle", "segments", "material_index"]

    def __init__(self, service, diameter, angle, segments, material_index):
        self.service = service
        self.diameter = float(diameter)
        self.angle = float(angle)
        self.segments = int(segments)
        self.material_index = int(material_index) - 1

    def _execute(self, context):
        return self.service.calculate_elbow_unfolding(self.diameter, self.angle, self.segments, self.material_index)
