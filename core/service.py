from abc import ABC
from app.context import AppContext
from core.events import Event, EventType

class Service(ABC):
    def __init__(self, context: AppContext):
        self.context = context
        self.commands = {}

    def register_command(self, name: str, command_cls):
        self.commands[name] = command_cls
        self.context.events.emit(
            Event(EventType.COMMAND_AVAILABLE, service_name=self.__class__.displayed_name, name=name, command_cls=command_cls)
        )

    def get_command_params(self, command_name: str):
        command_cls = self.commands.get(command_name)
        if command_cls:
            return command_cls.get_params(self)
        return []

    def emit_event(self, event):
        if hasattr(self.context, "events") and self.context.events:
            self.context.events.emit(event)


