import unittest
from app.context import AppContext
from core.events import EventDispatcher
from modules.about.service import AboutService
from modules.about.commands import GetAboutCreatorCommand, GetAboutProgramCommand, SendFeedbackCommand

from core.response import Response, TextBox

class TestAboutModule(unittest.TestCase):
    def setUp(self):
        self.context = AppContext()
        self.context.events = EventDispatcher()
        self.service = AboutService(self.context)

    def test_get_about_creator(self):
        result = self.service.get_about_creator()
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Кручківський Юрій Олександрович", result.boxes[0].text)

    def test_get_about_program(self):
        result = self.service.get_about_program()
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("ПРОГРАМА", result.boxes[0].text)

    def test_get_about_creator_command(self):
        command = GetAboutCreatorCommand(self.service)
        result = command._execute(self.context)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Кручківський Юрій Олександрович", result.boxes[0].text)

    def test_get_about_program_command(self):
        command = GetAboutProgramCommand(self.service)
        result = command._execute(self.context)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("ПРОГРАМА", result.boxes[0].text)

    def test_send_feedback_command(self):
        command = SendFeedbackCommand(self.service, "Test feedback")
        result = command._execute(self.context)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Дякуємо", result.boxes[0].text)

if __name__ == "__main__":
    unittest.main()
