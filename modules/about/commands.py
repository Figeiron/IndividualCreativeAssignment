from core.command import Command
from abc import ABC
from core.parameter import ParameterSchema
from UI.common.presentation.hint import LargeTextHint, OrderHint


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


class SendFeedbackCommand(Command):
    name = "Надіслати відгук"
    description = "Надішліть свій відгук про програму"

    @classmethod
    def get_params(cls, service):
        return [
            ParameterSchema(
                name="feedback_text",
                display_name="Ваш відгук",
                description="Напишіть ваші враження або пропозиції"
            ).with_hints([LargeTextHint(), OrderHint(1)]).build()
        ]

    def __init__(self, service, feedback_text):
        self.service = service
        self.feedback_text = feedback_text

    def _execute(self, context):
        return self.service.send_feedback(self.feedback_text)
