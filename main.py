from app.application import Application
from app.context import AppContext

from core.events import EventDispatcher

from modules.about.service import AboutService
from modules.metal_calc.service import MetalCalcService

from UI.console.ConsoleViewer import ConsoleViewer

context = AppContext()
context.events = EventDispatcher()

app = Application(context)
viewer = ConsoleViewer(context)

context.events.subscribe(app)
context.events.subscribe(viewer)

about_service = AboutService(context)
metal_service = MetalCalcService(context)

app.register_service(about_service.displayed_name, about_service)
app.register_service(metal_service.displayed_name, metal_service)

app.run()
