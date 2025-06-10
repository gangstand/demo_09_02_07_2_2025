from app.infrastructure.database.postgresql.models import MaterialType
from app.infrastructure.database.postgresql.repository.material_type import MaterialTypeRepository

class MaterialTypeService:
    def __init__(self):
        self.repo = MaterialTypeRepository()

    def get_all(self) -> list[MaterialType]:
        return self.repo.get_all()

    def get_by_id(self, material_type_id: int) -> MaterialType:
        mt = self.repo.get_by_id(material_type_id)
        if not mt:
            raise ValueError(f"MaterialType с id={material_type_id} не найден")
        return mt

    def create(self, name: str, loss_percent: float = 0.0) -> MaterialType:
        return self.repo.add(name, loss_percent)
