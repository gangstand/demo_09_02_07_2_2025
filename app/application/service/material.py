from app.infrastructure.database.postgresql.models import Material
from app.infrastructure.database.postgresql.repository.material import MaterialRepository

class MaterialService:
    def __init__(self):
        self.repo = MaterialRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, material_id: int):
        m = self.repo.get_by_id(material_id)
        if not m:
            raise ValueError(f"Материал {material_id} не найден")
        return m

    def create(self, **data):
        material = Material(**data)
        return self.repo.add(material)

    def update(self, material_id: int, **data):
        return self.repo.update(material_id, **data)

    @staticmethod
    def calc_min_batch_cost(material: Material) -> float:
        if material.quantity >= material.min_quantity:
            return 0.0
        missing = material.min_quantity - material.quantity
        packs = (missing + material.pack_size - 1) // material.pack_size
        batch_qty = packs * material.pack_size
        cost = batch_qty * float(material.price)
        return round(cost, 2)

    def get_by_name(self, name: str) -> Material:
        m = self.repo.get_by_name(name)
        if not m:
            raise ValueError(f"Материал с именем '{name}' не найден")
        return m