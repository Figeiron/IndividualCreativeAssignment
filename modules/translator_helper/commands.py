from core.command import Command


class TranslateTextCommand(Command):
    name = "Перекласти текст"
    description = "Перекласти текст"
    expected_params = ["text"]

    def __init__(self, service, text: str):
        self.service = service
        self.text = text

    def _execute(self, context):
        return self.service.translate_text(self.text)


class SetSourceLanguageCommand(Command):
    name = "Встановити мову джерела"
    description = "Встановити мову джерела"
    expected_params = ["lang"]

    def __init__(self, service, lang: str):
        self.service = service
        self.lang = lang

    def _execute(self, context):
        return self.service.set_source_language(self.lang)


class SetTargetLanguageCommand(Command):
    name = "Встановити мову перекладу"
    description = "Встановити мову перекладу"
    expected_params = ["lang"]

    def __init__(self, service, lang: str):
        self.service = service
        self.lang = lang

    def _execute(self, context):
        return self.service.set_target_language(self.lang)


class ShowLanguagesCommand(Command):
    name = "Показати поточні мови"
    description = "Показати поточні мови"
    expected_params = []

    def __init__(self, service):
        self.service = service

    def _execute(self, context):
        return self.service.show_languages()


class DetectLanguageCommand(Command):
    name = "Визначити мову тексту"
    description = "Визначити мову тексту"
    expected_params = ["text"]

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
