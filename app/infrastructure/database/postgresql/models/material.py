from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class Material(Base):
    __tablename__ = 'materials'
    __table_args__ = (
        {"comment": "Материалы на складе: основной справочник"},
    )

    id = Column(
        Integer,
        primary_key=True,
        comment="PK — уникальный идентификатор материала"
    )
    name = Column(
        String(100),
        nullable=False,
        comment="Наименование материала"
    )
    description = Column(
        String,
        nullable=True,
        comment="Описание материала"
    )
    image_path = Column(
        String,
        nullable=True,
        comment="Путь к изображению материала"
    )
    material_type_id = Column(
        Integer,
        ForeignKey('material_types.id'),
        nullable=False,
        comment="FK → material_types.id"
    )
    unit_id = Column(
        Integer,
        ForeignKey('units.id'),
        nullable=False,
        comment="FK → units.id"
    )
    quantity = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Текущее количество на складе"
    )
    min_quantity = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Минимально допустимое количество"
    )
    pack_size = Column(
        Integer,
        nullable=False,
        default=1,
        comment="Количество единиц в одной упаковке"
    )
    price = Column(
        Numeric(10, 2),
        nullable=False,
        default=0.00,
        comment="Цена за единицу материала"
    )

    material_type = relationship("MaterialType", lazy="joined")
    unit = relationship("Unit", lazy="joined")

    material_suppliers = relationship(
        "MaterialSupplier",
        back_populates="material",
        cascade="all, delete-orphan"
    )

    suppliers = relationship(
        "Supplier",
        secondary="material_suppliers",
        viewonly=True,
        lazy="joined"
    )
