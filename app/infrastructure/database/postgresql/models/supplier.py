from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class Supplier(Base):
    __tablename__ = 'suppliers'
    __table_args__ = (
        {"comment": "Справочник поставщиков сырья"},
    )

    id = Column(
        Integer,
        primary_key=True,
        comment="PK — уникальный идентификатор поставщика"
    )
    name = Column(
        String(100),
        nullable=False,
        comment="Наименование поставщика"
    )
    inn = Column(
        String(12),
        nullable=False,
        unique=True,
        comment="ИНН поставщика"
    )

    material_suppliers = relationship(
        "MaterialSupplier",
        back_populates="supplier",
        cascade="all, delete-orphan"
    )

    materials = relationship(
        "Material",
        secondary="material_suppliers",
        viewonly=True
    )
