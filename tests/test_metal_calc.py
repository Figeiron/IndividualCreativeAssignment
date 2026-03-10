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

class TestMetalCalcModule(unittest.TestCase):
    def setUp(self):
        self.context = AppContext()
        self.context.events = EventDispatcher()
        self.service = MetalCalcService(self.context)

    def test_get_materials(self):
        result = self.service.get_materials()
        self.assertIn("Сталь (S235) 1мм: 450.0 грн/м2", result)
        self.assertIn("Алюміній 1.5мм: 950.0 грн/м2", result)

    def test_calculate_pipe_unfolding(self):
        # Diameter 100, Length 1000, Material 1 (S235 1mm - 450.0)
        # Width = 100 * pi = 314.16
        # Area = 0.31416 * 1 = 0.31416 m2
        # Cost = 0.31416 * 450 = 141.37
        result = self.service.calculate_pipe_unfolding(100, 1000, 0)
        self.assertIn("Розгортка: 314.16 x 1000 мм", result)
        self.assertIn("Площа: 0.314 м2", result)
        self.assertIn("Вартість: 141.37 грн", result)

    def test_calculate_pipe_command(self):
        # User enters 1 for the first material
        command = CalculatePipeCommand(self.service, "100", "1000", "1")
        result = command.execute(self.context)
        self.assertIn("Розгортка: 314.16 x 1000.0 мм", result)
        self.assertIn("Вартість: 141.37 грн", result)

    def test_calculate_elbow_unfolding(self):
        # Diameter 100, Angle 90, Segments 3, Material 1 (S235 1mm - 450.0)
        # R = 1.5 * 100 = 150
        # Arc length = (150 * 2 * pi) * (90/360) = 300 * pi * 0.25 = 75 * pi = 235.62
        # Area = (100 * pi / 1000) * (235.62 / 1000) = 0.31416 * 0.23562 = 0.07402 m2
        # Cost = 0.07402 * 450 = 33.31
        result = self.service.calculate_elbow_unfolding(100, 90, 3, 0)
        self.assertIn("Приблизна площа: 0.074 м2", result)
        self.assertIn("Приблизна вартість: 33.31 грн", result)

    def test_get_materials_command(self):
        command = GetMaterialsCommand(self.service)
        result = command.execute(self.context)
        self.assertIn("Сталь (S235) 1мм", result)

if __name__ == "__main__":
    unittest.main()
