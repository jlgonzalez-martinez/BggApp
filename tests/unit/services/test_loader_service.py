from unittest.mock import MagicMock

import pytest

from boardgame.adapters.clients.dto import (
    BoardgameDto,
    ExpansionDto,
    PlayerDto,
    LanguageDependenceDto,
)
from boardgame.domain.commands import LoadBoardgame
from boardgame.domain.model import Category, Mechanic, Family
from boardgame.services.loader_service import LoaderService
from tests.unit.fakes import FakeUnitOfWork, FakeBggClient


class TestLoaderService:
    """Test LoaderService class."""

    @pytest.fixture(scope="class")
    def bgg_id(self) -> int:
        """Fake Bgg id."""
        return 1

    @pytest.fixture(scope="class")
    def category(self) -> str:
        """Fake category."""
        return "category"

    @pytest.fixture(scope="class")
    def family(self) -> str:
        """Fake family."""
        return "family"

    @pytest.fixture(scope="class")
    def mechanic(self) -> str:
        """Fake mechanic."""
        return "mechanic"

    @pytest.fixture(scope="class")
    def boardgame_dto(self, bgg_id, mechanic, family, category) -> BoardgameDto:
        """Fake Bgg id."""
        return BoardgameDto(
            bgg_id=bgg_id,
            name="Test Boardgame",
            description="Test description",
            image_url="url",
            year_published=2020,
            min_players=1,
            max_players=2,
            playing_time=30,
            min_play_time=10,
            max_play_time=30,
            min_age=10,
            rating_average=9.1,
            weight_average=3.5,
            mechanics=[mechanic],
            categories=[category],
            families=[family],
            expansions=[ExpansionDto(bgg_id=2, name="expansion")],
            players=[PlayerDto(number=1, best=10, recommended=20, not_recommended=0)],
            language_dependence=LanguageDependenceDto(
                very_low=1, low=2, medium=3, high=4, very_high=5
            ),
        )

    @pytest.mark.unit
    def test_load_boardgame(self, bgg_id, boardgame_dto, category, family, mechanic):
        """Test load boardgame."""
        bgg_client = FakeBggClient(boardgame_dto)
        unit_of_work = FakeUnitOfWork()
        loader_service = LoaderService(MagicMock(), bgg_client, unit_of_work)
        loader_service(LoadBoardgame(bgg_id=bgg_id))

        boardgame = unit_of_work.boardgames.get(bgg_id)

        assert boardgame.name == boardgame_dto.name
        assert boardgame.description == boardgame_dto.description
        assert boardgame.stat.weight_average == boardgame_dto.weight_average
        assert boardgame.stat.rating_average == boardgame_dto.rating_average
        assert boardgame.categories == [Category(name=category)]
        assert boardgame.mechanics == [Mechanic(name=mechanic)]
        assert boardgame.families == [Family(name=family)]
        assert bgg_client.bgg_id == bgg_id
        assert unit_of_work.categories.get(category).name == category
        assert unit_of_work.families.get(family).name == family
        assert unit_of_work.mechanics.get(mechanic).name == mechanic
