from datetime import datetime
from fastapi import FastAPI
from schema.anime import AnimeFull

app = FastAPI()


@app.get("/")
async def root():
    return AnimeFull(
        id=0,
        user_id=0,
        name="TEst",
        create_time=datetime.now(),
        watched_time=None,
        downloaded=False,
        watched=False,
        rating=None,
        url=None,
        remark="Mark",
        tmdb_id=None,
        tags=[],
        categories=[],
        comment="Comment")