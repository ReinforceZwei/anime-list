from fastapi import Depends
from typing import Annotated

from dal.user import UserDao

def db_session():
    return ""

def user_dao(db: Annotated[str, Depends(db_session)]):
    return UserDao(db)