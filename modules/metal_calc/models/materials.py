from dataclasses import dataclass
from itertools import count
from os import name
from typing import Optional


class AutoID:
    def __init_subclass__(cls):
        cls._id_gen = count(1)

    def _next_id(self):
        return next(self._id_gen)


@dataclass
class MetalMaterial(AutoID):
    name: str
    price_per_m2: float
    salary_per_m2: float
    id: Optional[int] = None

    def __post_init__(self):
        if not self.id:
            self.id = self._next_id()


THIN_METALS = [
    MetalMaterial(name="Сталь (S235) 1мм", price_per_m2=450.0, salary_per_m2=50),
    MetalMaterial(name="Сталь (S235) 2мм", price_per_m2=850.0, salary_per_m2=55),
    MetalMaterial(name="Нержавіюча сталь 1мм", price_per_m2=1200.0, salary_per_m2=60),
    MetalMaterial(name="Алюміній 1.5мм", price_per_m2=950.0, salary_per_m2=65)
]
