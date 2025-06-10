from sqlalchemy import Column, Integer, String

from .base import Base

class Unit(Base):
    __tablename__ = 'units'
    __table_args__ = (
        {"comment": "Справочник единиц измерения материалов"},
    )

    id = Column(
        Integer,
        primary_key=True,
        comment="PK — уникальный идентификатор единицы измерения"
    )
    name = Column(
        String(50),
        nullable=False,
        unique=True,
        comment="Название единицы измерения"
    )
