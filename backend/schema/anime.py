from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .tag import Tag
from .category import Category

# Base anime model
class AnimeBase(BaseModel):
    id: int
    user_id: int
    name: str
    create_time: datetime
    watched_time: Optional[datetime]
    downloaded: bool
    watched: bool
    rating: Optional[int]
    #comment: str
    url: Optional[str]
    remark: Optional[str]
    tmdb_id: Optional[str]
    tags: list[Tag]
    categories: list[Category]

# Anime model with comment
class AnimeFull(AnimeBase):
    comment: Optional[str]

# Anime model for frontend listing (no need comment)
class AnimeShort(AnimeBase):
    pass