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

# get /anime get details
# post /anime create new anime
# patch /anime update anime
# delete /anime delete anime
# get /anime/tag get tags
# patch /anime/tag link tags to anime
# delete /anime/tag delete linked tags
# get /anime/category get category
# patch /anime/category link category to anime
# delete /anime/category delete linked category

# get /tags get all tags
# get /tag get tag details
# get /tag/anime get anime with this tag
# post /tag create tag
# patch /tag update tag
# delete /tag delete tag

# get /categories get all categories
# get /category get category details
# get /category/anime get anime in this category
# post /category create category
# patch /category update category
# delete /category delete category

# get /user get user details
# post /user create new user
# post /user/login login user
# get /user/settings get user settings
# patch /user/settings update user settings