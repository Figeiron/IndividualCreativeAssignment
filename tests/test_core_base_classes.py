import unittest
from unittest.mock import MagicMock
from core.service import Service
from core.command import Command
from core.events import EventType, Event

class MockContext:
    def __init__(self):
        self.events = MagicMock()

class MockCommand(Command):
    name = "TestCommand"
    description = "A test command"
    
    @classmethod
    def get_params(cls, service):
        return ["param1"]

    def _execute(self, context):
        return "result"

class MockService(Service):
    displayed_name = "MockService"

class TestCoreBaseClasses(unittest.TestCase):
    def setUp(self):
        self.context = MockContext()
        self.service = MockService(self.context)

    def test_service_registration(self):
        self.service.register_command(MockCommand.name, MockCommand)
        self.assertIn(MockCommand.name, self.service.commands)
        
        # Check if event was emitted
        self.context.events.emit.assert_called()
        args, kwargs = self.context.events.emit.call_args
        event = args[0]
        self.assertEqual(event.type, EventType.COMMAND_AVAILABLE)
        self.assertEqual(event.data["name"], MockCommand.name)

    def test_get_command_params(self):
        self.service.register_command(MockCommand.name, MockCommand)
        params = self.service.get_command_params(MockCommand.name)
        self.assertEqual(params, ["param1"])
        
        params_none = self.service.get_command_params("NonExistent")
        self.assertEqual(params_none, [])

    def test_command_execution_success(self):
        command = MockCommand()
        command.execute(self.context)
        
        # Check if COMMAND_EXECUTED event was emitted
        self.context.events.emit.assert_called()
        # Find the COMMAND_EXECUTED call
        calls = self.context.events.emit.call_args_list
        found = False
        for call in calls:
            event = call[0][0]
            if event.type == EventType.COMMAND_EXECUTED:
                self.assertEqual(event.data["command"], "TestCommand")
                self.assertEqual(event.data["result"], "result")
                found = True
        self.assertTrue(found)

    def test_command_execution_failure(self):
        class FailingCommand(Command):
            def _execute(self, context):
                raise Exception("Test error")
        
        command = FailingCommand()
        command.execute(self.context)
        
        # Check if ERROR event was emitted
        calls = self.context.events.emit.call_args_list
        found = False
        for call in calls:
            event = call[0][0]
            if event.type == EventType.ERROR:
                self.assertEqual(event.data["error_message"], "Test error")
                found = True
        self.assertTrue(found)

if __name__ == '__main__':
    unittest.main()
