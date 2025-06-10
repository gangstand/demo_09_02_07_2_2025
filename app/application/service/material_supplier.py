from app.infrastructure.database.postgresql.repository.material_supplier import MaterialSupplierRepository


class MaterialSupplierService:
    def __init__(self):
        self.repo = MaterialSupplierRepository()

    def attach(self, material_id: int, supplier_id: int, rating: float, start_date):
        return self.repo.add(material_id, supplier_id, rating, start_date)

    def detach(self, material_id: int, supplier_id: int):
        self.repo.remove(material_id, supplier_id)

    def list(self, material_id: int):
        return self.repo.list_for_material(material_id)
