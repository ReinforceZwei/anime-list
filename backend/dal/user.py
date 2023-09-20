from fastapi import Depends
from typing import Annotated

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.user import User, UserLogin, UserRead, UserSettings, UserSettingsUpdate
from core.utils import generate_update_sql
from core.config import settings

class UserDao(BaseDao):
    def create(self, name: str, password_hash: str):
        user_id = self.exec('INSERT INTO user(name, password) VALUES (%s, %s)', (name, password_hash)).lastrowid
        user_setting = [
            user_id,
            settings.default_title,
            settings.default_watched_title,
            settings.default_unwatched_title]
        self.exec('INSERT INTO user_setting VALUES(%s, %s, %s, %s)', user_setting)
        return self.get(user_id)
    
    def exists(self, id: int) -> bool:
        return self.row_exist('user', 'id = %s', (id,))
    
    def get(self, user_id: int) -> User:
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE id = %s', (user_id,)).fetchone()
        )

    def get_by_name(self, name: str) -> User:
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE name = %s', (name,)).fetchone()
        )
    
    def get_settings(self, user_id: int) -> UserSettings:
        return UserSettings.model_validate(
            self.exec('SELECT * FROM user_setting WHERE user_id = %s', (user_id,)).fetchone()
        )
    
    def update_settings(self, user_id: int, settings: UserSettingsUpdate):
        settings_dict = settings.model_dump(exclude_none=True)
        sql = generate_update_sql('user_setting', settings_dict, 'user_id = %s')
        self.exec(sql, [*settings_dict.values(), user_id]).rowcount