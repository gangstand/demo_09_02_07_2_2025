from app.infrastructure.database.postgresql.models import ProductType
from app.infrastructure.database.postgresql.repository import ProductTypeRepository


class ProductTypeService:
    def __init__(self):
        self.repo = ProductTypeRepository()

    def get_all(self) -> list[ProductType]:
        return self.repo.get_all()

    def get_by_id(self, product_type_id: int) -> ProductType:
        pt = self.repo.get_by_id(product_type_id)
        if not pt:
            raise ValueError(f"ProductType с id={product_type_id} не найден")
        return pt

    def create(self, name: str, coefficient: float) -> ProductType:
        return self.repo.add(name=name, coefficient=coefficient)
