from abc import ABC, abstractmethod
from core.events import Event, EventType


class Command(ABC):
    name: str = "unknown"
    description: str = "unknown"

    def execute(self, context):
        try:
            result = self._execute(context)
            context.events.emit(Event(EventType.COMMAND_EXECUTED, command=self.name, result=result))

        except Exception as e:
            context.events.emit(Event(EventType.ERROR, error_message=str(e)))

    @classmethod
    def get_params(cls, service):
        pass

    @abstractmethod
    def _execute(self, context):
        pass
