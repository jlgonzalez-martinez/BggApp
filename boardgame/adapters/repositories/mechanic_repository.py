from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, Optional

from boardgame.domain.model import Mechanic

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class MechanicAbstractRepository(ABC):
    """Boardgame Abstract Repository"""

    def __init__(self):
        self.seen = set()  # type: Set["Mechanic"]

    def add(self, mechanic: "Mechanic"):
        """Add a mechanic to the repository"""
        self._add(mechanic)
        self.seen.add(mechanic)

    def get(self, name: str) -> Optional["Mechanic"]:
        """Get a mechanic by its name"""
        mechanic = self._get(name)
        if mechanic:
            self.seen.add(mechanic)
        return mechanic

    @abstractmethod
    def _add(self, mechanic: "Mechanic"):
        raise NotImplementedError

    @abstractmethod
    def _get(self, name: str) -> "Mechanic":
        raise NotImplementedError


class MechanicSqlAlchemyRepository(MechanicAbstractRepository):
    """Mechanic Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def _add(self, mechanic: "Mechanic"):
        self._session.add(mechanic)

    def _get(self, name: str) -> "Mechanic":
        return self._session.query(Mechanic).filter_by(name=name).first()
