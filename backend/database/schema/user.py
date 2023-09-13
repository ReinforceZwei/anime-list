# from typing import Optional
# from sqlmodel import SQLModel, Field, Relationship
# from datetime import datetime
# from core.config import settings

# class UserBase(SQLModel):
#     name: str = Field(unique=True)
#     password: str

# class User(UserBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     create_time: datetime = Field(default_factory=datetime.now)

# class UserSettings(SQLModel, table=True):
#     user: User = Relationship()
#     user_id: Optional[int] = Field(default=None, primary_key=True, foreign_key="user.id")
#     title: str = Field(default=settings.default_title)
#     title_watched: str = Field(default=settings.default_watched_title)
#     title_unwatched: str = Field(default=settings.default_unwatched_title)

# class UserCreate(UserBase):
#     pass

