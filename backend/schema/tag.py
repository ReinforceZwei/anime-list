from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str = Field(unique=True)
    color: str

class AnimeTag(SQLModel, table=True):
    anime_id: Optional[int] = Field(
        default=None, foreign_key="anime.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )