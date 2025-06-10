from sqlalchemy import select
from app.infrastructure.database.postgresql.session import SessionLocal
from app.infrastructure.database.postgresql.models import Supplier, MaterialSupplier

class SupplierRepository:
    @staticmethod
    def get_all():
        with SessionLocal() as session:
            return session.scalars(select(Supplier)).all()

    @staticmethod
    def get_by_id(supplier_id: int):
        with SessionLocal() as session:
            return session.get(Supplier, supplier_id)

    @staticmethod
    def get_by_material(material_id: int):
        with SessionLocal() as session:
            stmt = (
                select(Supplier, MaterialSupplier.rating, MaterialSupplier.start_date)
                .join(MaterialSupplier, Supplier.id == MaterialSupplier.supplier_id)
                .where(MaterialSupplier.material_id == material_id)
            )
            return session.execute(stmt).unique().all()


    @staticmethod
    def add(supplier: Supplier):
        with SessionLocal() as session:
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier

    @staticmethod
    def update(supplier: Supplier):
        with SessionLocal() as session:
            merged = session.merge(supplier)
            session.commit()
            return merged

    @staticmethod
    def delete(supplier_id: int):
        with SessionLocal() as session:
            s = session.get(Supplier, supplier_id)
            if s:
                session.delete(s)
                session.commit()
