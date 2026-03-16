import math
from dataclasses import dataclass
from modules.metal_calc.models.materials import MetalMaterial


@dataclass
class Product:
    diameter_mm: float
    material: MetalMaterial
    has_salary: bool

    def get_area_m2(self) -> float:
        raise NotImplementedError

    def get_salary(self) -> float:
        raise NotImplementedError

    def get_cost(self) -> float:
        return (self.get_area_m2() * self.material.price_per_m2) + (self.get_salary() if self.has_salary else 0)


@dataclass
class Pipe(Product):
    length_mm: float

    def get_salary(self) -> float:
        return self.get_area_m2() * 50

    def get_width_mm(self) -> float:
        return self.diameter_mm * math.pi

    def get_area_m2(self) -> float:
        width_m = self.get_width_mm() / 1000
        length_m = self.length_mm / 1000
        return width_m * length_m

    def __str__(self):
        return (f"Виріб: Труба (Діаметр: {self.diameter_mm} мм, Довжина: {self.length_mm} мм)\n"
                f"Розгортка: {self.get_width_mm():.2f} x {self.length_mm} мм\n"
                f"Матеріал: {self.material.name}\n"
                f"Площа: {self.get_area_m2():.3f} м2\n"
                f"Вартість: {self.get_cost():.2f} грн")


@dataclass
class Elbow(Product):
    angle_deg: float
    segments: int

    def get_salary(self) -> float:
        return self.get_area_m2() * 50

    def get_radius_bend(self) -> float:
        return self.diameter_mm * 1.5

    def get_arc_length_mm(self) -> float:
        return (self.get_radius_bend() * 2 * math.pi) * (self.angle_deg / 360)

    def get_area_m2(self) -> float:
        width_m = (self.diameter_mm * math.pi) / 1000
        arc_length_m = self.get_arc_length_mm() / 1000
        return width_m * arc_length_m

    def __str__(self):
        return (f"Виріб: Коліно (Діаметр: {self.diameter_mm} мм, Кут: {self.angle_deg}°, Сегментів: {self.segments})\n"
                f"Матеріал: {self.material.name}\n"
                f"Приблизна площа: {self.get_area_m2():.3f} м2\n"
                f"Приблизна вартість: {self.get_cost():.2f} грн\n"
                f"(Розрахунок базується на середній довжині дуги при R=1.5D)")
