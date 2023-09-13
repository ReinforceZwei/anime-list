from pydantic import BaseModel

class UserLogin(BaseModel):
    pass

class UserRead(BaseModel):
    id: int

class UserSettings(BaseModel):
    pass