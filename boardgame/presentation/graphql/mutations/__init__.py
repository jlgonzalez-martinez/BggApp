import strawberry

from .boardgame import BoardgameMutations


@strawberry.type
class Mutation(BoardgameMutations):
    pass
