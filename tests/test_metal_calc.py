import unittest
import math
from app.context import AppContext
from core.events import EventDispatcher
from modules.metal_calc.service import MetalCalcService
from modules.metal_calc.commands import (
    GetMaterialsCommand,
    CalculatePipeCommand,
    CalculateElbowCommand
)

from core.response import Response, TextBox

class TestMetalCalcModule(unittest.TestCase):
    def setUp(self):
        self.context = AppContext()
        self.context.events = EventDispatcher()
        self.service = MetalCalcService(self.context)

    def test_get_materials(self):
        result = self.service.get_materials()
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Сталь (S235) 1мм: 450.0 грн/м2", result.boxes[0].text)
        self.assertIn("Алюміній 1.5мм: 950.0 грн/м2", result.boxes[0].text)

    def test_calculate_pipe_unfolding(self):
        # Diameter 100, Length 1000, Material id 1 (S235 1mm - 450.0)
        # Width = 100 * pi = 314.16
        # Area = 0.31416 * 1 = 0.31416 m2
        # Cost = 0.31416 * 450 = 141.37
        result = self.service.calculate_pipe_unfolding(100, 1000, 1, False)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Розгортка: 314.16 x 1000 мм", result.boxes[0].text)
        self.assertIn("Площа: 0.314 м2", result.boxes[0].text)
        self.assertIn("Вартість: 141.37 грн", result.boxes[0].text)

    def test_calculate_pipe_command(self):
        # User enters 1 for the first material id 1
        command = CalculatePipeCommand(self.service, False, 1, 100.0, 1000.0)
        result = command._execute(self.context)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Розгортка: 314.16 x 1000.0 мм", result.boxes[0].text)
        self.assertIn("Вартість: 141.37 грн", result.boxes[0].text)

    def test_calculate_elbow_unfolding(self):
        # Diameter 100, Angle 90, Segments 3, Material id 1 (S235 1mm - 450.0)
        # R = 1.5 * 100 = 150
        # Arc length = (150 * 2 * pi) * (90/360) = 300 * pi * 0.25 = 75 * pi = 235.62
        # Area = (100 * pi / 1000) * (235.62 / 1000) = 0.31416 * 0.23562 = 0.07402 m2
        # Cost = 0.07402 * 450 = 33.31
        result = self.service.calculate_elbow_unfolding(100, 90, 3, 1, False)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Приблизна площа: 0.074 м2", result.boxes[0].text)
        self.assertIn("Приблизна вартість: 33.31 грн", result.boxes[0].text)

    def test_get_materials_command(self):
        command = GetMaterialsCommand(self.service)
        result = command._execute(self.context)
        self.assertIsInstance(result, Response)
        self.assertIsInstance(result.boxes[0], TextBox)
        self.assertIn("Сталь (S235) 1мм", result.boxes[0].text)

if __name__ == "__main__":
    unittest.main()
