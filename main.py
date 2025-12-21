from app.application import Application
from app.context import AppContext

from core.events import EventDispatcher

from modules.translator_helper.service import TranslatorHelperService
from modules.about.service import AboutService

from utils.TriggerListener import TriggerListener
from UI.console.ConsoleViewer import ConsoleViewer

context = AppContext()
context.events = EventDispatcher()

app = Application(context)
viewer = ConsoleViewer(context)
trigger = TriggerListener(context)

context.events.subscribe(app)
context.events.subscribe(viewer)
context.events.subscribe(trigger)

about_service = AboutService(context)
t_h_service = TranslatorHelperService(context)
app.register_service(t_h_service.displayed_name, t_h_service)
app.register_service(about_service.displayed_name, about_service)

app.run()
