from core.command import Command


class GetAboutCreatorCommand(Command):
    name = "Про розробника"
    description = "Про розробника"

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_about_creator()


class GetAboutProgramCommand(Command):
    name = "Про програму"
    description = "Про програму"

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_about_program()
