from core.command import Command
from abc import ABC


class GetAboutCommand(Command, ABC):
    def __init__(self, service):
        self.service = service

class GetAboutCreatorCommand(GetAboutCommand):
    name = "Про розробника"
    description = "Про розробника"

    def __init__(self, service):
        super().__init__(service)

    def _execute(self, context):
        return self.service.get_about_creator()


class GetAboutProgramCommand(GetAboutCommand):
    name = "Про програму"
    description = "Про програму"

    def __init__(self, service):
        super().__init__(service)

    def _execute(self, context):
        return self.service.get_about_program()
