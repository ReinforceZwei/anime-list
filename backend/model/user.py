from .base import RequestModel, ResponseModel, DatabaseModel

class User(DatabaseModel):
    id: int
    name: str
    password: str # This is hashed

class UserLogin(RequestModel):
    name: str
    password: str

class UserRead(RequestModel):
    id: int

class UserSettings(ResponseModel):
    user_id: int
    title: str
    title_watched: str
    title_unwatched: str