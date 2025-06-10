from sqlalchemy import Column, Integer, String, Float

from .base import Base

class ProductType(Base):
    __tablename__ = 'product_types'
    __table_args__ = (
        {"comment": "Справочник типов продукции: коэффициент расхода сырья"},
    )

    id = Column(
        Integer,
        primary_key=True,
        comment="PK — уникальный идентификатор типа продукции"
    )
    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Название типа продукции"
    )
    coefficient = Column(
        Float,
        nullable=False,
        default=1.0,
        comment="Коэффициент типа продукции для расчёта расхода сырья"
    )
