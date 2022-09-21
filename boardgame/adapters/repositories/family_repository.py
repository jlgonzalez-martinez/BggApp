from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, Optional

from boardgame.domain.model import Family

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class FamilyAbstractRepository(ABC):
    """Boardgame Abstract Repository"""

    def __init__(self):
        self.seen = set()  # type: Set["Family"]

    def add(self, family: "Family"):
        """Add a family to the repository"""
        self._add(family)
        self.seen.add(family)

    def get(self, name: str) -> Optional["Family"]:
        """Get a family by its name"""
        family = self._get(name)
        if family:
            self.seen.add(family)
        return family

    @abstractmethod
    def _add(self, family: "Family"):
        raise NotImplementedError

    @abstractmethod
    def _get(self, name: str) -> "Family":
        raise NotImplementedError


class FamilySqlAlchemyRepository(FamilyAbstractRepository):
    """Family Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def _add(self, family: "Family"):
        self._session.add(family)

    def _get(self, name: str) -> "Family":
        return self._session.query(Family).filter_by(name=name).first()
