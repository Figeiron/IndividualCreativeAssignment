from dataclasses import dataclass

@dataclass
class MetalMaterial:
    name: str
    price_per_m2: float

THIN_METALS = [
    MetalMaterial("Сталь (S235) 1мм", 450.0),
    MetalMaterial("Сталь (S235) 2мм", 850.0),
    MetalMaterial("Нержавіюча сталь 1мм", 1200.0),
    MetalMaterial("Алюміній 1.5мм", 950.0)
]
