import unittest
import os
from app.context import AppContext
from core.events import EventDispatcher, Event, EventType
from core.response import Response, TextBox, TableBox, TableCell, PlotBox
from modules.excel_export.service import ExcelExportService

class TestExcelExport(unittest.TestCase):
    def setUp(self):
        self.context = AppContext()
        self.context.events = EventDispatcher()
        self.service = ExcelExportService(self.context)
        self.test_filename = "test_export.xlsx"

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_export_no_data(self):
        response = self.service.export_last_response(self.test_filename)
        self.assertIn("Немає даних", response.boxes[0].text)

    def test_export_with_data(self):
        # Mock a command execution result
        test_response = Response(boxes=[
            TextBox(text="Test Title"),
            TableBox(cells=[
                TableCell(pos=(0, 0), text="Header 1"),
                TableCell(pos=(0, 1), text="Header 2"),
                TableCell(pos=(1, 0), text="Value 1"),
                TableCell(pos=(1, 1), text="Value 2"),
            ]),
            PlotBox(plot_points=[(1, 10), (2, 20), (3, 30)])
        ])
        
        event = Event(EventType.COMMAND_EXECUTED, result=test_response)
        self.service.handle_event(event)
        
        response = self.service.export_last_response(self.test_filename)
        self.assertIn("успішно експортовано", response.boxes[0].text)
        self.assertTrue(os.path.exists(self.test_filename))

if __name__ == "__main__":
    unittest.main()
