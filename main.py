from app.application import Application
from app.context import AppContext

from core.events import EventDispatcher

from modules.about.service import AboutService
from modules.metal_calc.service import MetalCalcService
from modules.excel_export.service import ExcelExportService

from UI.gui.TkinterViewer import TkinterViewer

context = AppContext()
context.events = EventDispatcher()

app = Application(context)
viewer = TkinterViewer(context)
excel_service = ExcelExportService(context)

context.events.subscribe(app)
context.events.subscribe(viewer)
context.events.subscribe(excel_service)

about_service = AboutService(context)
metal_service = MetalCalcService(context)

app.register_service(about_service.displayed_name, about_service)
app.register_service(metal_service.displayed_name, metal_service)
app.register_service(excel_service.displayed_name, excel_service)

app.run_with_gui(viewer)
