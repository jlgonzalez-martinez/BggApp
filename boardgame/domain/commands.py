"""Events module, this module contains all the boardgame events."""
from dataclasses import dataclass


class Command:
    """Event base class"""

    pass


@dataclass
class LoadBoardgame(Command):
    """Load boardgame command"""

    bgg_id: int
