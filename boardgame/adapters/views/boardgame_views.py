from typing import List, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from boardgame.domain.model import Boardgame
from config import settings


class BoardgameViews:
    """Boardgame views to retrieve data."""

    def get_all(self) -> List[Boardgame]:
        """Get all boardgames."""
        raise NotImplementedError


class BoardgameSqlAlchemyViews(BoardgameViews):
    """Boardgame views to retrieve data."""

    def __init__(self):
        super().__init__()
        self.engine = create_engine(
            f"postgresql://{settings.database.user}:{settings.database.password}"
            f"@{settings.database.host}:{settings.database.port}/{settings.database.database}",
            isolation_level="REPEATABLE READ",
        )
        self._session = sessionmaker(bind=self.engine)()

    def get_all(self, start: int = None, end: int = None) -> List[Boardgame]:
        """Get all boardgames."""
        boardgames = self._session.query(Boardgame)
        if start and end:
            boardgames = boardgames.slice(start, end)
        else:
            boardgames = boardgames.all()
        return boardgames

    def get(self, bgg_id: int) -> Optional[Boardgame]:
        """Get a boardgame by its bgg_id."""
        return self._session.query(Boardgame).filter_by(bgg_id=bgg_id).first()
