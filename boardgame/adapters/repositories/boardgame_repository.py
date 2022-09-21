from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Set, Optional

from boardgame.domain.model import Boardgame

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class BoardgameAbstractRepository(ABC):
    """Boardgame Abstract Repository"""

    def __init__(self):
        self.seen = set()  # type: Set["Boardgame"]

    def add(self, boardgame: "Boardgame"):
        """Add a boardgame to the repository"""
        self._add(boardgame)
        self.seen.add(boardgame)

    def get(self, bgg_id: int) -> Optional["Boardgame"]:
        """Get an aggregate by its bgg_id"""
        boardgame = self._get(bgg_id)
        if boardgame:
            self.seen.add(boardgame)
        return boardgame

    @abstractmethod
    def _add(self, boardgame: "Boardgame"):
        raise NotImplementedError

    @abstractmethod
    def _get(self, bgg_id: int) -> "Boardgame":
        raise NotImplementedError


class BoardgameSqlAlchemyRepository(BoardgameAbstractRepository):
    """Boardgame Repository"""

    def __init__(self, session: "Session"):
        super().__init__()
        self._session = session

    def _add(self, boardgame: "Boardgame"):
        self._session.add(boardgame)

    def _get(self, bgg_id: int) -> "Boardgame":
        return self._session.query(Boardgame).filter_by(bgg_id=bgg_id).first()
