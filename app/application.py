from core.service import Service
from core.events import Event, EventType


class Application:
    def __init__(self, context):
        self.context = context
        self.services = {}
        self.running = False

    def handle_event(self, event):
        if event.type == EventType.EXIT:
            self.running = False

    def register_service(self, name: str, service: Service):
        self.context.events.emit(Event(EventType.SERVICE_AVAILABLE, service_name=name, service=service))
        self.services[name] = service

    def run_command(self, command):
        return command.execute(self.context)

    def run(self):
        self.running = True

        self.context.events.emit(Event(EventType.START))

        while self.running:
            if not self.context.events.has_events():
                self.context.events.emit(Event(EventType.IDLE))

            self.context.events.dispatch()