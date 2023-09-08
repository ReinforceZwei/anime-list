from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserBase(SQLModel):
    name: str
    password: str

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    create_time: datetime = Field(default_factory=datetime.now)

class UserCreate(UserBase):
    pass