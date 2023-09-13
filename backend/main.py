from datetime import datetime
from fastapi import FastAPI, APIRouter

from core.config import settings

from router import user

print(settings.dict())

import database.init

app = FastAPI()

api = APIRouter(prefix='/api')
api.include_router(user.router)

app.include_router(api)

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