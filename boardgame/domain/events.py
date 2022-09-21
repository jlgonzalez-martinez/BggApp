"""Events module, this module contains all the boardgame events."""
from dataclasses import dataclass


class Event:
    """Event base class"""

    pass


@dataclass
class BoardgameCreated(Event):
    """Boardgame created event"""

    bgg_id: int
    name: str
    image_url: str
