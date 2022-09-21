from fastapi import FastAPI

from boardgame.bootstrap import bootstrap
from boardgame.domain.commands import LoadBoardgame

app = FastAPI()
bus = bootstrap()


@app.post("/boardgame/load/{bgg_id}")
def load_boardgame(bgg_id: int):
    """Load boardgame from the Boardgamegeek."""
    bus.handle(LoadBoardgame(bgg_id=bgg_id))
