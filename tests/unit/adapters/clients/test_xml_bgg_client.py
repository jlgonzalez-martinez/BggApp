import os
from http import HTTPStatus
from unittest.mock import MagicMock

import pytest

from boardgame.adapters.clients.dto import (
    PlayerDto,
    LanguageDependenceDto,
    ExpansionDto,
)
from boardgame.adapters.clients.exceptions import BoardgameGeekException
from boardgame.adapters.clients.xml_bgg_client import XmlBggClient
from config import TEST_RESOURCES
from tests.unit.fakes import FakeHttpClient


class TestXmlBggClient:
    """Test XML Bgg client class."""

    @pytest.fixture(scope="class")
    def url(self) -> str:
        """Bgg url."""
        return "https://boardgamegeek.com/"

    @pytest.fixture(scope="class")
    def logger(self) -> MagicMock:
        """Logger mock."""
        return MagicMock()

    @pytest.fixture(scope="class")
    def bgg_id(self) -> int:
        """Logger mock."""
        return 1

    @pytest.fixture
    def bgg_response(self):
        """XML response."""
        with open(os.path.join(TEST_RESOURCES, "boardgame.xml"), "r") as f:
            content = f.read()
        return content

    @pytest.mark.unit
    def test_non_ok_response(self, url, logger, bgg_id):
        """Test non 200 response."""
        http_client = FakeHttpClient(
            response=MagicMock(status_code=HTTPStatus.BAD_REQUEST)
        )
        client = XmlBggClient(api_url=url, logger=logger, http_client=http_client)
        with pytest.raises(BoardgameGeekException):
            client.get(bgg_id)
        assert http_client.url == url + str(bgg_id)

    @pytest.mark.unit
    def test_ok_response(self, url, logger, bgg_id, bgg_response):
        """Test non 200 response."""
        http_client = FakeHttpClient(
            response=MagicMock(status_code=HTTPStatus.OK, text=bgg_response)
        )
        client = XmlBggClient(api_url=url, logger=logger, http_client=http_client)
        loaded_boardgame = client.get(bgg_id)

        assert http_client.url == url + str(bgg_id)
        assert loaded_boardgame.bgg_id == 174430
        assert loaded_boardgame.name == "Gloomhaven"
        assert loaded_boardgame.image_url == "url"
        assert loaded_boardgame.description == "Test description"
        assert loaded_boardgame.year_published == 2017
        assert loaded_boardgame.min_players == 1
        assert loaded_boardgame.max_players == 4
        assert loaded_boardgame.playing_time == 120
        assert loaded_boardgame.min_play_time == 60
        assert loaded_boardgame.max_play_time == 120
        assert loaded_boardgame.min_age == 14
        assert loaded_boardgame.rating_average == 8.82222
        assert loaded_boardgame.weight_average == 3.8358
        assert loaded_boardgame.bayes_average == 8.56994
        assert loaded_boardgame.num_rates == 36743
        assert loaded_boardgame.num_weights == 1590
        assert loaded_boardgame.expansions == [
            ExpansionDto(
                bgg_id=310777,
                name="Gloomhaven: Beyond the End of the World (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=250337,
                name="Gloomhaven: Forgotten Circles",
            ),
            ExpansionDto(
                bgg_id=312635,
                name="Gloomhaven: No Pun Included 2019 Kickstarter (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=298195,
                name="Gloomhaven: Return of the Lost Cabal (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=312638,
                name="Gloomhaven: Secret Cabal 2020 Kickstarter (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=297586,
                name="Gloomhaven: Secrets of the Lost Cabal (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=226868,
                name="Gloomhaven: Solo Scenarios",
            ),
            ExpansionDto(
                bgg_id=310773,
                name="Gloomhaven: The Catacombs of Chaos (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=231934,
                name="Gloomhaven: The End of the World (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=300402,
                name="Gloomhaven: The Lucky Meeple (Promo Scenario)",
            ),
            ExpansionDto(
                bgg_id=310754,
                name="Gloomhaven: The Tower of Misfortune (Promo Scenario)",
            ),
        ]
        assert loaded_boardgame.players == [
            PlayerDto(number=1, best=107, recommended=410, not_recommended=207),
            PlayerDto(number=2, best=224, recommended=530, not_recommended=56),
            PlayerDto(number=3, best=474, recommended=317, not_recommended=24),
            PlayerDto(number=4, best=304, recommended=381, not_recommended=100),
        ]
        assert loaded_boardgame.language_dependence == LanguageDependenceDto(
            very_low=1, low=0, medium=2, high=35, very_high=12
        )
        assert loaded_boardgame.categories == [
            "Adventure",
            "Exploration",
            "Fantasy",
            "Fighting",
            "Miniatures",
        ]
        assert loaded_boardgame.mechanics == ["Action Queue", "Action Retrieval"]
        assert loaded_boardgame.families == [
            "Category: Dungeon Crawler",
            "Components: Miniatures",
            "Crowdfunding: Kickstarter",
            "Game: Gloomhaven",
        ]
