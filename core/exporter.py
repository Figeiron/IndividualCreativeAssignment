from abc import ABC, abstractmethod
from core.events import EventType
from core.response import Response

class Exporter(ABC):
    display_name: str = "Base Exporter"

    def __init__(self, context):
        self.context = context
        self.last_response = None
        
        self.context.events.subscribe(self)

    def handle_event(self, event):
        if event.type == EventType.COMMAND_EXECUTED:
            self.last_response = event.data.get("result")

    @abstractmethod
    def export(self, destination: str, data: Response):
        pass