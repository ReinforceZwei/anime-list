from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    password: str = Field(exclude=True)
    create_time: datetime