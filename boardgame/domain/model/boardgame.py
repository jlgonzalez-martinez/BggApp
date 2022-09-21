from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from boardgame.domain.model.aggregate import Aggregate
from boardgame.domain.model.stat import Stat
from boardgame.domain.model.language_dependence import LanguageDependence

if TYPE_CHECKING:
    from boardgame.domain.model.expansion import Expansion
    from boardgame.domain.model.category import Category
    from boardgame.domain.model.family import Family
    from boardgame.domain.model.mechanic import Mechanic
    from boardgame.domain.model.player import Player


@dataclass
class Boardgame(Aggregate):
    """Boardgame class implementation"""

    bgg_id: int = 0
    name: str = ""
    description: str = ""
    year_published: int = 0
    min_players: int = 0
    max_players: int = 0
    playing_time: int = 0
    min_play_time: int = 0
    max_play_time: int = 0
    min_age: int = 0
    image_url: str = ""
    stat: "Stat" = field(default_factory=Stat)
    language_dependence: "LanguageDependence" = field(
        default_factory=LanguageDependence
    )
    expansions: List["Expansion"] = field(default_factory=list)
    categories: List["Category"] = field(default_factory=list)
    mechanics: List["Mechanic"] = field(default_factory=list)
    families: List["Family"] = field(default_factory=list)
    players: List["Player"] = field(default_factory=list)

    def __hash__(self):
        return hash(self.bgg_id)
