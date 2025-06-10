from sqlalchemy import Column, Integer, String, Float

from .base import Base

class MaterialType(Base):
    __tablename__ = 'material_types'
    __table_args__ = (
        {"comment": "Справочник типов сырья: содержит процент потерь сырья"},
    )

    id = Column(
        Integer,
        primary_key=True,
        comment="PK — уникальный идентификатор типа сырья"
    )
    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Название типа сырья"
    )
    loss_percent = Column(
        Float,
        nullable=False,
        default=0.0,
        comment="Процент потери сырья при производстве"
    )
