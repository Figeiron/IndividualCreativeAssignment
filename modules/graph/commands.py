from core.command import Command


class ShowSchema(Command):
    name = "Показати схеми"
    description = "Показати схеми"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_schema_files()


class InitSchema(Command):
    name = "Завантажити схему"
    description = "Завантажити схему"
    expected_params = ["schema_index"]

    def __init__(self, service, schema_index):
        self.service = service
        self.schema_index = int(schema_index)

    def _execute(self, context):
        return self.service.pick_schema(self.schema_index)


class InitGraph(Command):
    name = "Завантажити граф"
    description = "Завантажити граф"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        self.service.setup_controller()
        self.service.setup_viewer()


class SetupGraph(Command):
    name = "Ініціалізувати граф"
    description = "Ініціалізувати граф"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        self.service.load_graph()
        self.service.setup_controller()
        return self.service.test_graph()


class SetupViewer(Command):
    name = "Запустити Viewer"
    description = "Запустити Viewer"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        self.service.setup_viewer()
