from boardgame.adapters.repositories import (
    BoardgameAbstractRepository,
    CategoryAbstractRepository,
    MechanicAbstractRepository,
    FamilyAbstractRepository,
)
from boardgame.services.unit_of_work import AbstractUnitOfWork


class FakeBoardgameRepository(BoardgameAbstractRepository):
    def __init__(self, boardgames):
        super().__init__()
        self._boardgames = set(boardgames)

    def _add(self, boardgame):
        self._boardgames.add(boardgame)

    def _get(self, bgg_id: int):
        return next((bg for bg in self._boardgames if bg.bgg_id == bgg_id), None)


class FakeCategoryRepository(CategoryAbstractRepository):
    def __init__(self, categories):
        super().__init__()
        self._categories = set(categories)

    def _add(self, category):
        self._categories.add(category)

    def _get(self, name: str):
        return next((c for c in self._categories if c.name == name), None)


class FakeMechanicRepository(MechanicAbstractRepository):
    def __init__(self, mechanics):
        super().__init__()
        self._mechanics = set(mechanics)

    def _add(self, mechanic):
        self._mechanics.add(mechanic)

    def _get(self, name: str):
        return next((m for m in self._mechanics if m.name == name), None)


class FakeFamilyRepository(FamilyAbstractRepository):
    def __init__(self, families):
        super().__init__()
        self._families = set(families)

    def _add(self, family):
        self._families.add(family)

    def _get(self, name: str):
        return next((f for f in self._families if f.name == name), None)


class FakeUnitOfWork(AbstractUnitOfWork):
    """In memory Unit of Work"""

    def __init__(self):
        self.boardgames = FakeBoardgameRepository([])
        self.categories = FakeCategoryRepository([])
        self.families = FakeFamilyRepository([])
        self.mechanics = FakeMechanicRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass
