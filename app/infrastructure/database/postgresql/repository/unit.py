from app.infrastructure.database.postgresql.session import SessionLocal
from app.infrastructure.database.postgresql.models import Unit

class UnitRepository:
    def __init__(self):
        self.session = SessionLocal()

    def get_all(self):
        return self.session.query(Unit).all()

    def add(self, name: str):
        unit = Unit(name=name)
        with self.session.begin():
            self.session.add(unit)
        return unit

    def close(self):
        self.session.close()
