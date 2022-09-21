from dataclasses import dataclass

from boardgame.adapters.clients.abstract_bgg_client import AbstractBggClient
from boardgame.adapters.clients.dto import BoardgameDto


@dataclass
class FakeBggClient(AbstractBggClient):
    """Fake HTTP client."""

    def __init__(self, boardgame_dto: BoardgameDto, exception=None):
        self.dto = boardgame_dto
        self.exception = exception
        self.bgg_id = None

    def get(self, bgg_id: int) -> BoardgameDto:
        """Fake get method."""
        self.bgg_id = bgg_id
        if self.exception:
            raise self.exception
        return self.dto
