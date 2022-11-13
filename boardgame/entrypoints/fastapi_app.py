from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from boardgame.bootstrap import bootstrap
from boardgame.domain.commands import LoadBoardgame
from boardgame.presentation.graphql.schema import schema

app = FastAPI()
bus = bootstrap()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.post("/boardgame/load/{bgg_id}")
def load_boardgame(bgg_id: int):
    """Load boardgame from the Boardgamegeek."""
    bus.handle(LoadBoardgame(bgg_id=bgg_id))
