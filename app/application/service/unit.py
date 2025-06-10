from app.infrastructure.database.postgresql.repository import UnitRepository


class UnitService:
    def __init__(self):
        self.repo = UnitRepository()

    def get_all(self):
        return self.repo.get_all()

    def create(self, name: str):
        return self.repo.add(name)