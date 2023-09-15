from .base import RequestModel, ResponseModel, DatabaseModel

class Tag(DatabaseModel):
    id: int
    user_id: int
    name: str
    color: str