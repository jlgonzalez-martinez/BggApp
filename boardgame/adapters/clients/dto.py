from dataclasses import dataclass, field
from typing import List


@dataclass
class ExpansionDto:
    """Expansion dto class."""

    bgg_id: int
    name: str
    description: str = ""


@dataclass
class PlayerDto:
    """Num players dto class"""

    number: int = 0
    best: int = 0
    recommended: int = 0
    not_recommended: int = 0


@dataclass
class LanguageDependenceDto:
    """Language dependence dto class"""

    very_low: int = 0
    low: int = 0
    medium: int = 0
    high: int = 0
    very_high: int = 0


@dataclass
class BoardgameDto:
    """Boardgame dto class"""

    bgg_id: int
    name: str
    description: str
    year_published: int = 0
    min_players: int = 0
    max_players: int = 0
    playing_time: int = 0
    min_play_time: int = 0
    max_play_time: int = 0
    min_age: int = 0
    image_url: str = ""
    std_dev: float = 0
    median: float = 0
    owned: int = 0
    trading: int = 0
    wanting: int = 0
    wishing: int = 0
    weight_average: float = 0
    rating_average: float = 0
    bayes_average: float = 0
    num_rates: int = 0
    num_comments: int = 0
    num_weights: int = 0
    expansions: List[ExpansionDto] = field(default_factory=list)
    language_dependence: LanguageDependenceDto = field(
        default_factory=LanguageDependenceDto
    )
    categories: List[str] = field(default_factory=list)
    mechanics: List[str] = field(default_factory=list)
    families: List[str] = field(default_factory=list)
    players: List[PlayerDto] = field(default_factory=list)
