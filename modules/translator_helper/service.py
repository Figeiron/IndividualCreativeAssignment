from libretranslatepy import LibreTranslateAPI
from core.service import Service
from modules.translator_helper.commands import *

class TranslatorHelperService(Service):
    displayed_name = "Перекладач"

    def __init__(self, context):
        super().__init__(context)
        self.SUPPORTED_LANGS = {"en", "uk", "de", "fr", "pl", "es"}

        self.api = LibreTranslateAPI("http://localhost:5000")

        try:
            self._call_api()
        except:
            raise BaseException("Немає LibreTranslate")

        self.source_lang = "en"
        self.target_lang = "uk"
        self.history = []

        self.register_command(TranslateTextCommand.name, TranslateTextCommand)
        self.register_command(SetSourceLanguageCommand.name, SetSourceLanguageCommand)
        self.register_command(SetTargetLanguageCommand.name, SetTargetLanguageCommand)
        self.register_command(ShowLanguagesCommand.name, ShowLanguagesCommand)
        self.register_command(ListLanguagesCommand.name, ListLanguagesCommand)
        self.register_command(DetectLanguageCommand.name, DetectLanguageCommand)
        self.register_command(ShowHistoryCommand.name, ShowHistoryCommand)
        self.register_command(ClearHistoryCommand.name, ClearHistoryCommand)


    def _call_api(self):
        self.api.languages()

    def translate_text(self, text: str):
        translated = self.api.translate(
            text,
            self.source_lang,
            self.target_lang
        )

        self.history.append({
            "source": self.source_lang,
            "target": self.target_lang,
            "text": text,
            "result": translated
        })

        return translated



    def set_source_language(self, lang: str):
        if lang not in self.SUPPORTED_LANGS and lang != "auto":
            raise ValueError(f"Непідтримувана мова: {lang}")
        self.source_lang = lang

        return f"Мова джерела встановлена: {lang}"

    def set_target_language(self, lang: str):
        self.target_lang = lang
        return f"Мова перекладу встановлена: {lang}"

    def show_languages(self):
        return {
            "source_language": self.source_lang,
            "target_language": self.target_lang
        }

    def detect_language(self, text: str):
        result = self.api.detect(text)
        return f'"language": {result[0]["language"]}'


    def list_history(self):
        if not self.history:
            return "Історія перекладів порожня"

        lines = []
        for i, item in enumerate(self.history, 1):
            lines.append(
                f"{i}. [{item['source']}→{item['target']}] "
                f"{item['text']} → {item['result']}"
            )

        return "\n".join(lines)

    def get_supported_languages(self):
        try:
            langs = self.api.languages()
            return "\n".join([
                f"{lang['code']}:\t{lang['name']}"
                for lang in langs
            ])
        except Exception as e:
            raise RuntimeError(f"Не вдалося отримати список мов: {e}")

    def clear_history(self):
        self.history.clear()
        return "Історія перекладів очищена"