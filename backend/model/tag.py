from typing import Optional
from .base import RequestModel, ResponseModel, DatabaseModel

class Tag(DatabaseModel):
    id: int
    user_id: int
    name: str
    color: Optional[str] = None

class TagCreate(RequestModel):
    name: str
    color: Optional[str] = None

class TagUpdate(RequestModel):
    name: Optional[str] = None
    color: Optional[str] = None