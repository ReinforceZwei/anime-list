from datetime import datetime
from fastapi import FastAPI, APIRouter

from core.config import settings

from router import user, anime, category, tag

print(settings.dict())

import database.init

app = FastAPI()

api = APIRouter(prefix='/api')
api.include_router(user.router)
api.include_router(anime.router)
api.include_router(category.router)
api.include_router(tag.router)

app.include_router(api)

@app.get("/")
async def root():
    return "If you see this, animelist is working"

