# from sqlmodel import SQLModel, Field, Relationship
# from typing import Optional

# class Category(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     user_id: int = Field(default=None, foreign_key="user.id")
#     name: str = Field(unique=True)
#     color: Optional[str]

# class AnimeCategory(SQLModel, table=True):
#     anime_id: Optional[int] = Field(
#         default=None, foreign_key="anime.id", primary_key=True
#     )
#     category_id: Optional[int] = Field(
#         default=None, foreign_key="category.id", primary_key=True
#     )