from sqlalchemy import select
from app.infrastructure.database.postgresql.session import SessionLocal
from app.infrastructure.database.postgresql.models import Material

class MaterialRepository:
    @staticmethod
    def get_all():
        with SessionLocal() as session:
            return session.scalars(select(Material)).unique().all()

    @staticmethod
    def get_by_id(material_id: int):
        with SessionLocal() as session:
            return session.get(Material, material_id)

    @staticmethod
    def add(material: Material):
        with SessionLocal() as session:
            session.add(material)
            session.commit()
            return material

    @staticmethod
    def update(material_id: int, **data):
        with SessionLocal() as session:
            m = session.get(Material, material_id)
            if not m:
                raise ValueError(f"Материал {material_id} не найден")

            for key, value in data.items():
                setattr(m, key, value)

            session.add(m)
            session.commit()
            session.refresh(m)
            return m

    @staticmethod
    def get_by_name(name: str) -> Material | None:
        with SessionLocal() as session:
            stmt = select(Material).where(Material.name == name)
            return session.scalars(stmt).first()