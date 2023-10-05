from typing import Optional
from .base import RequestModel, ResponseModel, DatabaseModel

class Category(DatabaseModel):
    id: int
    user_id: int
    name: str
    color: str

class CategoryUpdate(RequestModel):
    name: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(RequestModel):
    name: str
    color: Optional[str] = None