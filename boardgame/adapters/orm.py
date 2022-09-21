import logging

from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    ForeignKey,
    event,
    Text,
    Float,
)
from sqlalchemy.orm import mapper, relationship

from boardgame.domain.model import Category, Expansion, Boardgame
from boardgame.domain.model.family import Family
from boardgame.domain.model.language_dependence import LanguageDependence
from boardgame.domain.model.mechanic import Mechanic
from boardgame.domain.model.player import Player
from boardgame.domain.model.stat import Stat

logger = logging.getLogger(__name__)

metadata = MetaData()


boardgames = Table(
    "boardgames",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
    Column("bgg_id", Integer, nullable=False, unique=True),
    Column("name", String(250), nullable=False),
    Column("description", Text()),
    Column("year_published", Integer),
    Column("min_players", Integer),
    Column("max_players", Integer),
    Column("playing_time", Integer),
    Column("min_play_time", Integer),
    Column("max_play_time", Integer),
    Column("min_age", Integer),
    Column("image_url", String(250)),
)


expansion = Table(
    "expansions",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("bgg_id", Integer, nullable=False),
    Column("name", String(250)),
)

language_dependence = Table(
    "language_dependences",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("very_low", Integer),
    Column("low", Integer),
    Column("medium", Integer),
    Column("high", Integer),
    Column("very_high", Integer),
)

player = Table(
    "players",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("number", Integer),
    Column("best", Integer),
    Column("recommended", Integer),
    Column("not_recommended", Integer),
)

stat = Table(
    "stats",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("std_dev", Float),
    Column("median", Float),
    Column("trading", Integer),
    Column("wanting", Integer),
    Column("wishing", Integer),
    Column("weight_average", Float),
    Column("rating_average", Float),
    Column("bayes_average", Float),
    Column("num_rates", Integer),
    Column("num_comments", Integer),
    Column("num_weights", Integer),
)

mechanic = Table(
    "mechanics",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
    Column("name", String(100)),
    Column("description", Text()),
)

family = Table(
    "families",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
    Column("name", String(100)),
    Column("description", Text()),
)

category = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("version_number", Integer, nullable=False, server_default="0"),
    Column("name", String(100)),
    Column("description", Text()),
)


boardgame_category = Table(
    "boardgame_categories",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("category_id", Integer, ForeignKey("categories.id"), nullable=False),
)

boardgame_family = Table(
    "boardgame_families",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("family_id", Integer, ForeignKey("families.id"), nullable=False),
)


boardgame_mechanic = Table(
    "boardgame_mechanics",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("boardgame_id", Integer, ForeignKey("boardgames.id"), nullable=False),
    Column("mechanic_id", Integer, ForeignKey("mechanics.id"), nullable=False),
)


def start_mappers():
    """Start ORM mappers with the domain model classes."""
    logger.info("Starting ORM mappers")
    category_mapper = mapper(Category, category)
    expansion_mapper = mapper(Expansion, expansion)
    family_mapper = mapper(Family, family)
    language_dependence_mapper = mapper(LanguageDependence, language_dependence)
    mechanic_mapper = mapper(Mechanic, mechanic)
    player_mapper = mapper(Player, player)
    stat_mapper = mapper(Stat, stat)

    mapper(
        Boardgame,
        boardgames,
        properties={
            "expansions": relationship(expansion_mapper),
            "language_dependence": relationship(
                language_dependence_mapper, uselist=False
            ),
            "players": relationship(player_mapper),
            "stat": relationship(stat_mapper, uselist=False),
            "mechanics": relationship(mechanic_mapper, secondary=boardgame_mechanic),
            "families": relationship(family_mapper, secondary=boardgame_family),
            "categories": relationship(category_mapper, secondary=boardgame_category),
        },
    )


@event.listens_for(Boardgame, "load")
def receive_load(boardgame, _):
    boardgame.events = []
