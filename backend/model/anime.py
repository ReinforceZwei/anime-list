from typing import Optional, List
from datetime import datetime

from .base import RequestModel, ResponseModel, DatabaseModel
from .tag import Tag
from .category import Category

class Anime(DatabaseModel):
    id: int
    user_id: int
    create_time: datetime
    watched_time: Optional[datetime]
    downloaded: bool
    watched: bool
    rating: Optional[int]
    comment: Optional[str]
    url: Optional[str]
    remark: Optional[str]
    tmdb_id: Optional[str]
    tags: Optional[List[Tag]]
    category: Optional[List[Category]]

class AnimeCreate(RequestModel):
    name: str

class AnimeRead(RequestModel):
    id: int