from sqlalchemy import select

from app.infrastructure.database.postgresql.models import ProductType
from app.infrastructure.database.postgresql.session import SessionLocal


class ProductTypeRepository:
    @staticmethod
    def get_by_id(product_type_id: int) -> ProductType | None:
        with SessionLocal() as session:
            return session.get(ProductType, product_type_id)

    @staticmethod
    def get_all() -> list[ProductType]:
        with SessionLocal() as session:
            return session.scalars(select(ProductType)).all()

    @staticmethod
    def add(name: str, coefficient: float) -> ProductType:
        pt = ProductType(name=name, coefficient=coefficient)
        with SessionLocal() as session:
            session.add(pt)
            session.commit()
            session.refresh(pt)
            return pt
