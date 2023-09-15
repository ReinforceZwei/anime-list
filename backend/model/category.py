from .base import RequestModel, ResponseModel, DatabaseModel

class Category(DatabaseModel):
    id: int
    user_id: int
    name: str
    color: str