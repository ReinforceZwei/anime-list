from datetime import datetime
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse

from core.config import settings
import core.errors

from router import user, anime, category, tag

print(settings.model_dump())

import database.init

app = FastAPI()

@app.exception_handler(core.errors.DataNotFoundException)
async def data_not_found_exception_handler(request: Request, ex: core.errors.DataNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )

api = APIRouter(prefix='/api')
api.include_router(user.router)
api.include_router(anime.router)
api.include_router(category.router)
api.include_router(tag.router)

app.include_router(api)

@app.get("/")
async def root():
    return "If you see this, animelist is working"

