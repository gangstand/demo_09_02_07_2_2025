from app.infrastructure.database.postgresql.repository.supplier import SupplierRepository

class SupplierService:
    def __init__(self):
        self.repo = SupplierRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, supplier_id: int):
        s = self.repo.get_by_id(supplier_id)
        if not s:
            raise ValueError(f"Поставщик с id={supplier_id} не найден")
        return s

    def get_by_material(self, material_id: int):
        rows = self.repo.get_by_material(material_id)
        result = []
        for supplier, rating, start_date in rows:
            result.append({
                "supplier": supplier,
                "rating": rating,
                "start_date": start_date
            })
        return result

    def create(self, **data):
        from app.infrastructure.database.postgresql.models import Supplier
        sup = Supplier(**data)
        return self.repo.add(sup)

    def update(self, supplier_id: int, **data):
        sup = self.get_by_id(supplier_id)
        for k, v in data.items():
            setattr(sup, k, v)
        return self.repo.update(sup)

    def delete(self, supplier_id: int):
        self.get_by_id(supplier_id)
        self.repo.delete(supplier_id)
