from datetime import datetime
from fastapi import FastAPI
import database.model
from core.config import settings

print(settings.dict())


app = FastAPI()


@app.get("/")
async def root():
    return ""
    # return AnimeFull(
    #     id=0,
    #     user_id=0,
    #     name="TEst",
    #     create_time=datetime.now(),
    #     watched_time=None,
    #     downloaded=False,
    #     watched=False,
    #     rating=None,
    #     url=None,
    #     remark="Mark",
    #     tmdb_id=None,
    #     tags=[],
    #     categories=[],
    #     comment="Comment")