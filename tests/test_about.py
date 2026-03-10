import unittest
from app.context import AppContext
from core.events import EventDispatcher
from modules.about.service import AboutService
from modules.about.commands import GetAboutCreator, GetAboutProgram

class TestAboutModule(unittest.TestCase):
    def setUp(self):
        self.context = AppContext()
        self.context.events = EventDispatcher()
        self.service = AboutService(self.context)

    def test_get_about_creator(self):
        result = self.service.get_about_creator()
        self.assertIn("Кручківський Юрій Олександрович", result)

    def test_get_about_program(self):
        result = self.service.get_about_program()
        self.assertIn("ПРОГРАМА", result)
        self.assertIn("Програма помічник", result)

    def test_get_about_creator_command(self):
        command = GetAboutCreator(self.service)
        result = command.execute(self.context)
        self.assertIn("Кручківський Юрій Олександрович", result)

    def test_get_about_program_command(self):
        command = GetAboutProgram(self.service)
        result = command.execute(self.context)
        self.assertIn("ПРОГРАМА", result)

if __name__ == "__main__":
    unittest.main()
