from core.command import Command


class GetAboutCreator(Command):
    name = "Про розробника"
    description = "Про розробника"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_about_creator()


class GetAboutProgram(Command):
    name = "Про програму"
    description = "Про програму"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_about_program()

