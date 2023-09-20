from typing import Optional, List
from datetime import datetime
from pydantic import Field

from .base import RequestModel, ResponseModel, DatabaseModel
from .tag import Tag
from .category import Category

class Anime(DatabaseModel):
    id: int
    user_id: int
    name: str
    added_time: datetime
    watched_time: Optional[datetime]
    downloaded: bool
    watched: bool
    rating: Optional[int]
    comment: Optional[str]
    url: Optional[str]
    remark: Optional[str]
    tmdb_id: Optional[str]
    tags: Optional[List[Tag]] = Field(default_factory=list)
    category: Optional[List[Category]] = Field(default_factory=list)

class AnimeCreate(RequestModel):
    name: str

class AnimeRead(RequestModel):
    id: int

class AnimeUpdate(RequestModel):
    watched_time: Optional[datetime]
    downloaded: Optional[bool]
    watched: Optional[bool]
    rating: Optional[int]
    comment: Optional[str]
    url: Optional[str]
    remark: Optional[str]
    tmdb_id: Optional[str]