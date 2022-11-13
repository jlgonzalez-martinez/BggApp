import strawberry

from boardgame.presentation.graphql.queries.boardgame import BoardgameQueries


@strawberry.type
class Query(BoardgameQueries):
    pass
