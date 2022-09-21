from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from config import settings

from boardgame.adapters.repositories import (
    BoardgameAbstractRepository,
    CategoryAbstractRepository,
    FamilyAbstractRepository,
    MechanicAbstractRepository,
    BoardgameSqlAlchemyRepository,
    CategorySqlAlchemyRepository,
    FamilySqlAlchemyRepository,
    MechanicSqlAlchemyRepository,
)


class AbstractUnitOfWork(ABC):
    """Abstract Unit of Work"""

    def __init__(self):
        self.boardgames: Optional["BoardgameAbstractRepository"] = None
        self.categories: Optional["CategoryAbstractRepository"] = None
        self.families: Optional["FamilyAbstractRepository"] = None
        self.mechanics: Optional["MechanicAbstractRepository"] = None
        self.engine = None

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def collect_new_events(self):
        """TODO: Refactor this method"""
        for boardgame in self.boardgames.seen:
            while boardgame.events:
                yield boardgame.events.pop(0)
        for category in self.categories.seen:
            while category.events:
                yield category.events.pop(0)
        for family in self.families.seen:
            while family.events:
                yield family.events.pop(0)
        for mechanic in self.mechanics.seen:
            while mechanic.events:
                yield mechanic.events.pop(0)

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__()
        self.engine = create_engine(
            f"postgresql://{settings.database.user}:{settings.database.password}"
            f"@{settings.database.host}:{settings.database.port}/{settings.database.database}",
            isolation_level="REPEATABLE READ",
        )
        self.session_factory = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.boardgames = BoardgameSqlAlchemyRepository(self.session)
        self.categories = CategorySqlAlchemyRepository(self.session)
        self.families = FamilySqlAlchemyRepository(self.session)
        self.mechanics = MechanicSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
