import unittest
from core.events import Event, EventType, EventDispatcher

class TestListener:
    def __init__(self):
        self.received_events = []

    def handle_event(self, event):
        self.received_events.append(event)

class TestEvents(unittest.TestCase):
    def test_event_initialization(self):
        data = {"key": "value", "id": 1}
        event = Event(EventType.START, **data)
        self.assertEqual(event.type, EventType.START)
        self.assertEqual(event.data, data)

    def test_event_repr(self):
        event = Event(EventType.START, key="value")
        self.assertEqual(repr(event), "Event: START: {'key': 'value'}")

    def test_event_dispatcher_emit_and_next(self):
        dispatcher = EventDispatcher()
        event1 = Event(EventType.START)
        event2 = Event(EventType.IDLE)
        
        self.assertFalse(dispatcher.has_events())
        dispatcher.emit(event1)
        self.assertTrue(dispatcher.has_events())
        dispatcher.emit(event2)
        
        self.assertEqual(dispatcher.next_event(), event1)
        self.assertEqual(dispatcher.next_event(), event2)
        self.assertIsNone(dispatcher.next_event())
        self.assertFalse(dispatcher.has_events())

    def test_event_dispatcher_subscribe_and_dispatch(self):
        dispatcher = EventDispatcher()
        listener = TestListener()
        dispatcher.subscribe(listener)
        
        event = Event(EventType.START, message="Hello")
        dispatcher.emit(event)
        
        dispatcher.dispatch()
        self.assertEqual(len(listener.received_events), 1)
        self.assertEqual(listener.received_events[0], event)

    def test_dispatch_empty_queue(self):
        dispatcher = EventDispatcher()
        listener = TestListener()
        dispatcher.subscribe(listener)
        
        dispatcher.dispatch()
        self.assertEqual(len(listener.received_events), 0)

if __name__ == '__main__':
    unittest.main()
