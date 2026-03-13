from core.command import Command
from core.parameter import Parameter


class TranslateTextCommand(Command):
    name = "Перекласти текст"
    description = "Перекласти обраний текст"
    expected_params = [
        Parameter("text", "Текст", "текст для перекладу", str)
    ]

    def __init__(self, service, text: str):
        self.service = service
        self.text = text

    def _execute(self, context):
        return self.service.translate_text(self.text)


class SetSourceLanguageCommand(Command):
    name = "Встановити мову джерела"
    description = "Змінити мову, з якої здійснюється переклад"
    
    @staticmethod
    def parse_lang(v: str) -> str:
        v = v.strip().lower()
        if not v:
            raise ValueError("Мова не може бути порожньою")
        return v

    expected_params = [
        Parameter("lang", "Код мови", "наприклад: uk, en, auto", parse_lang)
    ]

    def __init__(self, service, lang: str):
        self.service = service
        self.lang = lang

    def _execute(self, context):
        return self.service.set_source_language(self.lang)


class SetTargetLanguageCommand(Command):
    name = "Встановити мову перекладу"
    description = "Змінити мову, на яку здійснюється переклад"
    
    @staticmethod
    def parse_lang(v: str) -> str:
        v = v.strip().lower()
        if v == "auto":
            raise ValueError("Цільова мова не може бути 'auto'")
        if not v:
            raise ValueError("Мова не може бути порожньою")
        return v

    expected_params = [
        Parameter("lang", "Код мови", "наприклад: uk, en", parse_lang)
    ]

    def __init__(self, service, lang: str):
        self.service = service
        self.lang = lang

    def _execute(self, context):
        return self.service.set_target_language(self.lang)


class ShowLanguagesCommand(Command):
    name = "Показати поточні мови"
    description = "Показати встановлені мови джерела та перекладу"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.show_languages()


class DetectLanguageCommand(Command):
    name = "Визначити мову тексту"
    description = "Автоматично визначити мову заданого тексту"
    expected_params = [
        Parameter("text", "Текст", "текст для аналізу", str)
    ]

    def __init__(self, service, text: str):
        self.service = service
        self.text = text

    def _execute(self, context):
        return self.service.detect_language(self.text)


class ShowHistoryCommand(Command):
    name = "Показати історію перекладів"
    description = "Показати історію перекладів"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.list_history()


class ClearHistoryCommand(Command):
    name = "Очистити історію перекладів"
    description = "Очистити історію перекладів"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.clear_history()

class ListLanguagesCommand(Command):
    name = "Показати доступні мови"
    description = "Показати доступні мови"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.get_supported_languages()
