import unittest
from app.context import AppContext
from core.events import EventDispatcher
from modules.about.service import AboutService
from modules.about.commands import GetAboutCreatorCommand, GetAboutProgramCommand, SendFeedbackCommand

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

    def test_get_about_creator_command(self):
        command = GetAboutCreatorCommand(self.service)
        result = command._execute(self.context)
        self.assertIn("Кручківський Юрій Олександрович", result)

    def test_get_about_program_command(self):
        command = GetAboutProgramCommand(self.service)
        result = command._execute(self.context)
        self.assertIn("ПРОГРАМА", result)

    def test_send_feedback_command(self):
        command = SendFeedbackCommand(self.service, "Test feedback")
        result = command._execute(self.context)
        self.assertIn("Дякуємо", result)

if __name__ == "__main__":
    unittest.main()
