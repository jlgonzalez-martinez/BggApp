from typing import List, TYPE_CHECKING

import strawberry

from .category import CategoryType
from .domain_type import DomainType
from .expansion import ExpansionType
from .family import FamilyType
from .language_dependence import LanguageDependenceType
from .mechanic import MechanicType
from .player import PlayerType
from .stat import StatType

if TYPE_CHECKING:
    from boardgame.domain.model import Boardgame


@strawberry.type
class BoardgameType(DomainType):
    """Boardgame type"""

    id: strawberry.ID
    bgg_id: int
    name: str
    description: str
    year_published: int
    min_players: int
    max_players: int
    playing_time: int
    min_play_time: int
    max_play_time: int
    min_age: int
    image_url: str
    stat: "StatType"
    language_dependence: "LanguageDependenceType"
    expansions: List["ExpansionType"]
    categories: List["CategoryType"]
    mechanics: List["MechanicType"]
    families: List["FamilyType"]
    players: List["PlayerType"]

    @classmethod
    def from_domain(cls, instance: "Boardgame") -> "BoardgameType":
        if instance:
            return cls(
                id=getattr(instance, "id", None),
                bgg_id=instance.bgg_id,
                name=instance.name,
                description=instance.description,
                year_published=instance.year_published,
                min_players=instance.min_players,
                max_players=instance.max_players,
                playing_time=instance.playing_time,
                min_play_time=instance.min_play_time,
                max_play_time=instance.max_play_time,
                min_age=instance.min_age,
                image_url=instance.image_url,
                stat=StatType.from_domain(instance.stat),
                language_dependence=LanguageDependenceType.from_domain(
                    instance.language_dependence
                ),
                expansions=[
                    ExpansionType.from_domain(expansion)
                    for expansion in instance.expansions
                ],
                categories=[
                    CategoryType.from_domain(category)
                    for category in instance.categories
                ],
                mechanics=[
                    MechanicType.from_domain(mechanic)
                    for mechanic in instance.mechanics
                ],
                families=[
                    FamilyType.from_domain(family) for family in instance.families
                ],
                players=[PlayerType.from_domain(player) for player in instance.players],
            )
