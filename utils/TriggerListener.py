from collections import deque
from core.events import EventType, Event


class TriggerListener:
    def __init__(self, context):
        self.context = context
        self.correct_order = [
            "Визначити мову тексту",
            "Перекласти текст",
            "Визначити мову тексту"
        ]
        self.sequence = deque(maxlen=len(self.correct_order))

    def handle_event(self, event):
        if event.type == EventType.COMMAND_EXECUTED:
            cmd = event.data["command"]

            self.sequence.append(cmd)
            if list(self.sequence) == self.correct_order:
                self.trigger()

    def trigger(self):
        self.context.events.emit(
            Event(
                EventType.EASTER_EGG,
                message="Великодка активована!"
            )
        )
