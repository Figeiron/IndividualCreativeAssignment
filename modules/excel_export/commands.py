from core.command import Command
from core.parameter import ParameterSchema

FILENAME = ParameterSchema(
    name="filename",
    display_name="Ім'я файлу",
    description="Введіть назву файлу для експорту (наприклад, report.xlsx)",
    parse_type=str
)

class ExportToExcelCommand(Command):
    name = "Експортувати останню відповідь"
    description = "Зберігає останній отриманий результат у файл Excel"

    @classmethod
    def get_params(cls, service):
        return [FILENAME.build()]

    def __init__(self, service, filename):
        self.service = service
        self.filename = filename

    def _execute(self, context):
        return self.service.export_last_response(self.filename)
