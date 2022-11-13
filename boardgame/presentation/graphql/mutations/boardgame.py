import strawberry

from boardgame.adapters.views.boardgame_views import BoardgameSqlAlchemyViews
from boardgame.bootstrap import bootstrap
from boardgame.domain.commands import LoadBoardgame
from boardgame.presentation.graphql.types.boardgame import BoardgameType

bus = bootstrap(start_orm=False)


@strawberry.type
class BoardgameMutations:
    """Boardgame mutations."""

    @strawberry.mutation
    def load_from_bgg(self, bgg_id: int) -> BoardgameType:
        """Load boardgame from the Boardgamegeek."""
        bus.handle(LoadBoardgame(bgg_id=bgg_id))
        boardgame = BoardgameSqlAlchemyViews().get(bgg_id)
        return BoardgameType.from_domain(boardgame)
