from typing import Optional
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

class UserInfo(ResponseModel):
    id: int
    name: str

class UserTokenPair(ResponseModel):
    token: str
    refresh_token: str

class UserRefresh(RequestModel):
    refresh_token: str

class UserSettings(ResponseModel):
    user_id: int
    title: str
    title_watched: str
    title_unwatched: str

class UserSettingsUpdate(RequestModel):
    title: Optional[str]
    title_watched: Optional[str]
    title_unwatched: Optional[str]