from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

class MaterialSupplier(Base):
    __tablename__ = 'material_suppliers'
    __table_args__ = (
        {"comment": "Рейтинг и дата начала работы поставщика по конкретному материалу"},
    )

    material_id = Column(
        Integer,
        ForeignKey('materials.id', ondelete='CASCADE'),
        primary_key=True,
        comment="PK часть — материал"
    )
    supplier_id = Column(
        Integer,
        ForeignKey('suppliers.id', ondelete='CASCADE'),
        primary_key=True,
        comment="PK часть — поставщик"
    )
    rating = Column(
        Float,
        nullable=False,
        default=0.0,
        comment="Рейтинг качества поставки материала"
    )
    start_date = Column(
        Date,
        nullable=False,
        comment="Дата начала сотрудничества с поставщиком по данному материалу"
    )

    material = relationship(
        "Material",
        back_populates="material_suppliers",
        lazy="joined"
    )
    supplier = relationship(
        "Supplier",
        back_populates="material_suppliers",
        lazy="joined"
    )
