from typing import Optional

import strawberry

from boardgame.adapters.views.boardgame_views import BoardgameSqlAlchemyViews
from boardgame.presentation.graphql.pagination import (
    Connection,
    decode_cursor,
    get_paginated_response,
)
from boardgame.presentation.graphql.types.boardgame import BoardgameType


def get_boardgames(
    first: int = 20, after: Optional[str] = strawberry.UNSET
) -> Connection[BoardgameType]:
    """Get all boardgames."""
    start = decode_cursor(after) if after is not strawberry.UNSET else 0
    stop = start + first
    boardgames = BoardgameSqlAlchemyViews().get_all(start=start, end=stop)
    return get_paginated_response(boardgames, BoardgameType, first=first)


@strawberry.type
class BoardgameQueries:
    """Boardgame GraphQL queries."""

    boardgames: Connection[BoardgameType] = strawberry.field(resolver=get_boardgames)
