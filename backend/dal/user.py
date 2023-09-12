from fastapi import Depends
from sqlmodel import Session, select, insert, update
from typing import Annotated

from model.user import UserLogin
from database.schema.user import User

class UserDao:
    def __init__(self, db: Session):
        self._db = db
    
    def login(self, user: UserLogin):
        return self._db.exec(select(User).where(User.name == user.name)).one()
    
    def create(self, user: User):
        self._db.add(user)
        self._db.commit()
        return self._db.exec(select(User).where(User.name == user.name)).one()
    
    def get(self, user: User):
        return self._db.exec(select(User).where(User.id == user.id)).one()