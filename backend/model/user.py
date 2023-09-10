from pydantic import BaseModel
from database.schema.user import UserSettings

class UserLogin(BaseModel):
    name: str
    password: str

class UserRead(BaseModel):
    id: int

class UserSettings(UserSettings):
    pass