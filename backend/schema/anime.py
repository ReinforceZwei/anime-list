from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from .user import User
#from .tag import Tag
#from .category import Category

# All required fields for creating record
# Make it as base
class AnimeBase(SQLModel):
    name: str
    
# Real table schema that will be created in database
class Anime(AnimeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship()
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    create_time: datetime = Field(default_factory=datetime.now)
    watched_time: Optional[datetime]
    downloaded: bool = Field(default=False)
    watched: bool = Field(default=False)
    rating: Optional[int]
    comment: Optional[str]
    url: Optional[str]
    remark: Optional[str]
    tmdb_id: Optional[str]
    #tags: List[Tag]
    #categories: List[Category]

# Alias for base, used for create new record
class AnimeCreate(AnimeBase):
    pass

