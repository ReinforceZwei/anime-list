from fastapi import Depends
from typing import Annotated

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.user import User, UserLogin, UserRead

class UserDao(BaseDao):
    def create(self, user: UserLogin):
        user_id = self.exec('INSERT INTO user(name, password) VALUES (%s, %s)', (user.name, user.password)).lastrowid
        return self.get(UserRead(id=user_id))
    
    def get(self, user: UserRead):
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE id = %s', (user.id,)).fetchone()
        )

    def get_by_name(self, user: UserLogin):
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE name = %s', (user.name,)).fetchone()
        )