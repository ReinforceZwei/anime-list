from pydantic import BaseModel

class Category(BaseModel):
    id: int
    user_id: int
    name: str
    color: str