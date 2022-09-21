import logging

import pytest

from boardgame.adapters.clients.xml_bgg_client import XmlBggClient
from boardgame.domain.commands import LoadBoardgame
from boardgame.services.loader_service import LoaderService
from boardgame.services.unit_of_work import SqlAlchemyUnitOfWork


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("mappers")
class TestLoaderService:
    """Test the LoaderService."""

    @pytest.fixture(scope="class")
    def unit_of_work(self):
        """Loader service."""
        return SqlAlchemyUnitOfWork()

    @pytest.fixture(scope="class")
    def loader_service(self, unit_of_work):
        """Loader service."""
        return LoaderService(
            logger=logging.getLogger(__name__),
            bgg_client=XmlBggClient.build(),
            uow=unit_of_work,
        )

    @pytest.mark.integration
    def test_load_die_matcher_from_bgg(self, loader_service, unit_of_work):
        """Test loading a boardgame from BGG."""
        loader_service(LoadBoardgame(bgg_id=1))
        with unit_of_work:
            boardgame = unit_of_work.boardgames.get(1)
            assert boardgame.bgg_id == 1
            assert boardgame.name == "Die Macher"
            assert boardgame.stat
            assert boardgame.language_dependence
            assert boardgame.players
            assert boardgame.categories
            assert boardgame.mechanics
            assert boardgame.families
