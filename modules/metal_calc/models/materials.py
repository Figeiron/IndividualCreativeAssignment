from dataclasses import dataclass


@dataclass
class MetalMaterial:
    id: int
    name: str
    price_per_m2: float


THIN_METALS = [
    MetalMaterial(0, "Сталь (S235) 1мм", 450.0),
    MetalMaterial(1, "Сталь (S235) 2мм", 850.0),
    MetalMaterial(2, "Нержавіюча сталь 1мм", 1200.0),
    MetalMaterial(3, "Алюміній 1.5мм", 950.0)
]
