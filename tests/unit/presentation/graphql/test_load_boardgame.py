from unittest.mock import patch, MagicMock

import pytest

from boardgame.domain.commands import LoadBoardgame
from boardgame.domain.model import Boardgame
from boardgame.presentation.graphql.mutations import BoardgameMutations


@pytest.mark.unit
class TestLoadBoardgameMutation:
    """Boardgames query unit tests."""

    @pytest.fixture(scope="class")
    def bgg_id(self) -> int:
        """Boardgame type fixture."""
        return 1

    @pytest.fixture(scope="class")
    def boardgame(self, bgg_id):
        """Boardgames fixture."""
        return Boardgame(bgg_id=bgg_id)

    @pytest.fixture(scope="class")
    def boardgame_mutations(self):
        """Boardgames fixture."""
        return BoardgameMutations()

    @patch(
        "boardgame.presentation.graphql.mutations.boardgame.BoardgameSqlAlchemyViews"
    )
    @patch("boardgame.presentation.graphql.mutations.boardgame.bus")
    def test_get_boardgames(
        self, bus_mock, views_mock_class, boardgame_mutations, boardgame, bgg_id
    ):
        """Test load boardgame mutation."""
        views_mock = MagicMock()
        views_mock_class.return_value = views_mock
        views_mock.get.return_value = boardgame

        response = boardgame_mutations.load_from_bgg(bgg_id=bgg_id)

        bus_mock.handle.assert_called_once_with(LoadBoardgame(bgg_id=bgg_id))
        assert response.bgg_id == bgg_id
