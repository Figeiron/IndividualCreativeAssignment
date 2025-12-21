from enum import Enum, auto
from collections import deque

class EventType(Enum):
    START = auto()
    IDLE = auto()
    STEP = auto()
    FINISH = auto()
    UPDATE = auto()
    ERROR = auto()
    EXIT = auto()
    SERVICE_AVAILABLE = auto()
    SERVICE_SELECTED = auto()
    COMMAND_AVAILABLE = auto()
    SHOW_SERVICES_MENU = auto()
    COMMAND_SELECTED = auto()
    COMMAND_EXECUTED = auto()
    EXECUTE_COMMAND = auto()
    EASTER_EGG = auto()


class Event:
    def __init__(self, type_: EventType, **data):
        self.type = type_
        self.data = data

    def __repr__(self):
        return f"Event: {self.type.name}: {self.data}"


class EventDispatcher:
    def __init__(self):
        self._queue = deque()
        self._subscribers = []

    def has_events(self):
        return bool(self._queue)

    def emit(self, event):
        self._queue.append(event)

    def next_event(self):
        if self._queue:
            event = self._queue.popleft()
            return event
        return None

    def subscribe(self, listener):
        self._subscribers.append(listener)

    def dispatch(self):
        event = self.next_event()
        if not event:
            return
        for listener in self._subscribers:
            listener.handle_event(event)