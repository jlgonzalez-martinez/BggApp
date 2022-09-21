from logging import Logger
from typing import TYPE_CHECKING

from boardgame.adapters.clients.abstract_bgg_client import AbstractBggClient
from boardgame.domain.commands import LoadBoardgame
from boardgame.domain.events import BoardgameCreated
from boardgame.domain.model import (
    Boardgame,
    Stat,
    LanguageDependence,
    Expansion,
    Player,
    Mechanic,
    Family,
    Category,
)
from boardgame.domain.model.category import CategoryType
from boardgame.services.unit_of_work import AbstractUnitOfWork

if TYPE_CHECKING:
    from boardgame.adapters.clients.dto import BoardgameDto


class LoaderService:
    def __init__(
        self, logger: Logger, bgg_client: AbstractBggClient, uow: AbstractUnitOfWork
    ):
        self._logger = logger
        self._bgg_client = bgg_client
        self._uow = uow

    def __call__(self, cmd: LoadBoardgame):
        with self._uow:
            boardgame_dto = self._bgg_client.get(cmd.bgg_id)
            boardgame = Boardgame(
                bgg_id=boardgame_dto.bgg_id,
                name=boardgame_dto.name,
                description=boardgame_dto.description,
                year_published=boardgame_dto.year_published,
                min_players=boardgame_dto.min_players,
                max_players=boardgame_dto.max_players,
                playing_time=boardgame_dto.playing_time,
                min_play_time=boardgame_dto.min_play_time,
                max_play_time=boardgame_dto.max_play_time,
                min_age=boardgame_dto.min_age,
                image_url=boardgame_dto.image_url,
            )

            self.add_mechanics(boardgame, boardgame_dto)
            self.add_families(boardgame, boardgame_dto)
            self.add_categories(boardgame, boardgame_dto)
            self.add_stat(boardgame, boardgame_dto)
            self.add_expansions(boardgame, boardgame_dto)
            self.add_players(boardgame, boardgame_dto)
            self.add_language_dependence(boardgame, boardgame_dto)
            boardgame.events.append(
                BoardgameCreated(
                    bgg_id=boardgame.bgg_id,
                    name=boardgame.name,
                    image_url=boardgame.image_url,
                )
            )
            self._uow.boardgames.add(boardgame)
            self._uow.commit()

    def add_mechanics(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        for mechanic_name in boardgame_dto.mechanics:
            mechanic = self._uow.mechanics.get(mechanic_name)
            if not mechanic:
                mechanic = Mechanic(name=mechanic_name)
                self._uow.mechanics.add(mechanic)
            boardgame.mechanics.append(mechanic)

    def add_families(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        for family_name in boardgame_dto.families:
            family = self._uow.families.get(family_name)
            if not family:
                family = Family(name=family_name)
                self._uow.families.add(family)
            boardgame.families.append(family)

    def add_categories(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        for category_name in boardgame_dto.categories:
            category = self._uow.categories.get(category_name)
            if not category:
                category = Category(
                    name=category_name,
                    category_type=CategoryType.from_category(category_name),
                )
                self._uow.categories.add(category)
            boardgame.categories.append(category)

    def add_expansions(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        for expansion in boardgame_dto.expansions:
            boardgame.expansions.append(
                Expansion(name=expansion.name, bgg_id=expansion.bgg_id)
            )

    def add_players(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        for player in boardgame_dto.players:
            boardgame.players.append(
                Player(
                    number=player.number,
                    best=player.best,
                    recommended=player.recommended,
                    not_recommended=player.not_recommended,
                )
            )

    def add_stat(self, boardgame: Boardgame, boardgame_dto: "BoardgameDto"):
        boardgame.stat = Stat(
            std_dev=boardgame_dto.std_dev,
            median=boardgame_dto.median,
            owned=boardgame_dto.owned,
            trading=boardgame_dto.trading,
            wanting=boardgame_dto.wanting,
            wishing=boardgame_dto.wishing,
            weight_average=boardgame_dto.weight_average,
            rating_average=boardgame_dto.rating_average,
            bayes_average=boardgame_dto.bayes_average,
            num_rates=boardgame_dto.num_rates,
            num_comments=boardgame_dto.num_comments,
            num_weights=boardgame_dto.num_weights,
        )

    def add_language_dependence(
        self,
        boardgame: Boardgame,
        boardgame_dto: "BoardgameDto",
    ):
        boardgame.language_dependence = LanguageDependence(
            very_low=boardgame_dto.language_dependence.very_low,
            low=boardgame_dto.language_dependence.low,
            medium=boardgame_dto.language_dependence.medium,
            high=boardgame_dto.language_dependence.high,
            very_high=boardgame_dto.language_dependence.very_high,
        )
