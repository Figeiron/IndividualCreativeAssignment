import json
import os
from modules.metal_calc.models.materials import MetalMaterial, THIN_METALS


class MaterialsProvider:
    def __init__(self, filename="materials.json"):
        self.filename = os.path.join(os.path.dirname(__file__), filename)

    @property
    def thin_metals(self):
        return self.load_materials()

    def load_materials(self):
        if not os.path.exists(self.filename):
            self.save_materials(THIN_METALS)
            return THIN_METALS

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                materials = [MetalMaterial(**item) for item in data]
                return materials

        except (json.JSONDecodeError, TypeError, KeyError) as e:
            print(e)
            return THIN_METALS

    def save_materials(self, materials):
        data = [
            {
                "id": m.id,
                "name": m.name,
                "price_per_m2": m.price_per_m2,
                "salary_per_m2": m.salary_per_m2
            }
            for m in materials
        ]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
