from sqlalchemy import select
from app.infrastructure.database.postgresql.session import SessionLocal
from app.infrastructure.database.postgresql.models import MaterialType

class MaterialTypeRepository:
    @staticmethod
    def get_all() -> list[MaterialType]:
        with SessionLocal() as session:
            return session.scalars(select(MaterialType)).all()

    @staticmethod
    def get_by_id(material_type_id: int) -> MaterialType | None:
        with SessionLocal() as session:
            return session.get(MaterialType, material_type_id)

    @staticmethod
    def add(name: str, loss_percent: float = 0.0) -> MaterialType:
        mt = MaterialType(name=name, loss_percent=loss_percent)
        with SessionLocal() as session:
            session.add(mt)
            session.commit()
            session.refresh(mt)
            return mt
