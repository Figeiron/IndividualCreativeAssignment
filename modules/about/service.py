from core.service import Service
from core.response import Response, TextBox
from modules.about.commands import *


class AboutService(Service):
    displayed_name = "Про програму"

    def __init__(self, context):
        super().__init__(context)

        self.register_command(GetAboutCreatorCommand.name, GetAboutCreatorCommand)
        self.register_command(GetAboutProgramCommand.name, GetAboutProgramCommand)
        self.register_command(SendFeedbackCommand.name, SendFeedbackCommand)

    @staticmethod
    def get_about_creator():
        about_creator_text = (
            "Розробив студент групи Б25_F3(A)\n"
            "Кручківський Юрій Олександрович\n"
        )
        return Response(boxes=[TextBox(text=about_creator_text)])

    def get_about_program(self):
        about_program_text = (
            f"ПРОГРАМА <{self.context.data.get('app_name', 'Помічник')}>\n"
            "\n"
            "Це модульний асистент, побудований на базі\n"
            "подієво-орієнтованої архітектури.\n"
            "\n"
            "Основні можливості:\n"
            "• Динамічна реєстрація сервісів та команд.\n"
            "• Система глобальних подій та підписок.\n"
            "• Гнучке розширення функціоналу без зміни ядра.\n"
            "• Відстеження ланцюжків подій.\n"
            "\n"
            "Ви можете залишити відгук у відповідній команді меню."
        )
        return Response(boxes=[TextBox(text=about_program_text)])

    def send_feedback(self, text):
        print(f"Отримано відгук: {text}")
        return Response(boxes=[TextBox(text="Дякуємо за ваш відгук! Ми його обов'язково розглянемо.")])