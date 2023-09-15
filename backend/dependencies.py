from fastapi import Depends
from typing import Annotated

from database.connection import get_connection, PooledMySQLConnection
from dal.user import UserDao

def db_session() -> PooledMySQLConnection:
    db = get_connection()
    try:
        yield db
    finally:
        db.close()

def user_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return UserDao(db)