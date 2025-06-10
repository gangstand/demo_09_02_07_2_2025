from app.infrastructure.database.postgresql.repository import ProductTypeRepository, MaterialTypeRepository


class ProductionService:
    def __init__(self):
        self.pt_repo = ProductTypeRepository()
        self.mt_repo = MaterialTypeRepository()

    def calculate_output(
            self,
            product_type_id: int,
            material_type_id: int,
            qty: int,
            p1: float,
            p2: float
    ) -> int:
        pt = self.pt_repo.get_by_id(product_type_id)
        mt = self.mt_repo.get_by_id(material_type_id)
        if not pt or not mt or qty < 0 or p1 <= 0 or p2 <= 0:
            return -1

        base_need = p1 * p2 * pt.coefficient

        need_with_loss = base_need * (1 + mt.loss_percent / 100)

        if need_with_loss <= 0:
            return -1

        return int(qty // need_with_loss)
