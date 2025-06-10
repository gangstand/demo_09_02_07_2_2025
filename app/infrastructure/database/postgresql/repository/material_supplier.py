from sqlalchemy import select, delete
from app.infrastructure.database.postgresql.session import SessionLocal
from app.infrastructure.database.postgresql.models import MaterialSupplier

class MaterialSupplierRepository:
    @staticmethod
    def add(material_id: int, supplier_id: int, rating: float, start_date):
        ms = MaterialSupplier(
            material_id=material_id,
            supplier_id=supplier_id,
            rating=rating,
            start_date=start_date
        )
        with SessionLocal() as session:
            session.add(ms)
            session.commit()
            return ms

    @staticmethod
    def remove(material_id: int, supplier_id: int):
        with SessionLocal() as session:
            stmt = delete(MaterialSupplier).where(
                MaterialSupplier.material_id == material_id,
                MaterialSupplier.supplier_id == supplier_id
            )
            session.execute(stmt)
            session.commit()

    @staticmethod
    def list_for_material(material_id: int):
        with SessionLocal() as session:
            stmt = select(MaterialSupplier).where(
                MaterialSupplier.material_id == material_id
            )
            return session.scalars(stmt).all()
