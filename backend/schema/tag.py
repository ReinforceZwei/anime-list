from pydantic import BaseModel

class Tag(BaseModel):
    id: int
    user_id: int
    name: str
    color: str