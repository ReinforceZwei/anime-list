from pydantic import BaseModel
from database.schema.user import UserBase, UserSettings

class UserLogin(UserBase):
    pass

class UserRead(BaseModel):
    id: int

class UserSettings(UserSettings):
    pass