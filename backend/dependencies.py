from sqlmodel import Session
from fastapi import Depends
from typing import Annotated

from database.init import engine
from dal.user import UserDao

def db_session():
    return Session(engine)

def user_dao(db: Annotated[Session, Depends(db_session)]):
    return UserDao(db)