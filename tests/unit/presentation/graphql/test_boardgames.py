from unittest.mock import patch, MagicMock

import pytest

from boardgame.domain.model import Boardgame
from boardgame.presentation.graphql.queries.boardgame import get_boardgames
from boardgame.presentation.graphql.types.boardgame import BoardgameType


class TestBoardgamesQuery:
    """Boardgames query unit tests."""

    @pytest.fixture(scope="class")
    def boardgames(self):
        """Boardgames fixture."""
        return [Boardgame(bgg_id=1), Boardgame(bgg_id=2)]

    @pytest.fixture(scope="class")
    def first(self) -> int:
        """Boardgame type fixture."""
        return 5

    @patch("boardgame.presentation.graphql.queries.boardgame.BoardgameSqlAlchemyViews")
    @patch("boardgame.presentation.graphql.queries.boardgame.get_paginated_response")
    def test_get_boardgames(self, paginated_mock, views_mock_class, boardgames, first):
        """"""
        views_mock = MagicMock()
        views_mock_class.return_value = views_mock
        views_mock.get_all.return_value = boardgames
        paginated_mock.side_effect = lambda x, y, **kwargs: x

        boardgames = get_boardgames(first=first)
        views_mock.get_all.assert_called_once_with(start=0, end=5)
        paginated_mock.assert_called_once_with(boardgames, BoardgameType, first=first)
