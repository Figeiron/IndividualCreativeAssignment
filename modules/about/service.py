from core.service import Service
from modules.about.commands import *


class AboutService(Service):
    displayed_name = "Про програму"

    def __init__(self, context):
        super().__init__(context)

        self.register_command(GetAboutCreator.name, GetAboutCreator)
        self.register_command(GetAboutProgram.name, GetAboutProgram)

    @staticmethod
    def get_about_creator():
        about_creator_text = (
            "╔══════════════════════════════════════════════════════════╗\n"
            "║ Розробив студент групи Б25_F3(A)                         ║\n"
            "║ Кручківський Юрій Олександрович                          ║\n"
            "╚══════════════════════════════════════════════════════════╝"
        )
        return about_creator_text

    def get_about_program(self):
        about_program_text = (
            "╔══════════════════════════════════════════════════════════╗\n"
            f"║           ПРОГРАМА <{self.context.data.get('app_name', 'Помічник')}>                   ║\n"
            "╠══════════════════════════════════════════════════════════╣\n"
            "║ Це модульний асистент, побудований на базі               ║\n"
            "║ подієво-орієнтованої архітектури.                        ║\n"
            "║                                                          ║\n"
            "║ Основні можливості:                                      ║\n"
            "║ • Динамічна реєстрація сервісів та команд.               ║\n"
            "║ • Система глобальних подій та підписок.                  ║\n"
            "║ • Гнучке розширення функціоналу без зміни ядра.          ║\n"
            "║ • Відстеження ланцюжків подій.                           ║\n"
            "╚══════════════════════════════════════════════════════════╝"
        )
        return about_program_text