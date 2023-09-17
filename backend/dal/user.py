from fastapi import Depends
from typing import Annotated

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.user import User, UserLogin, UserRead, UserSettings, UserSettingsUpdate
from core.utils import generate_update_sql
from core.config import settings

class UserDao(BaseDao):
    def create(self, user: UserLogin):
        user_id = self.exec('INSERT INTO user(name, password) VALUES (%s, %s)', (user.name, user.password)).lastrowid
        user_setting = [
            user_id,
            settings.default_title,
            settings.default_watched_title,
            settings.default_unwatched_title]
        self.exec('INSERT INTO user_setting VALUES(%s, %s, %s, %s)', user_setting)
        return self.get(UserRead(id=user_id))
    
    def get(self, user: UserRead) -> User:
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE id = %s', (user.id,)).fetchone()
        )

    def get_by_name(self, user: UserLogin) -> User:
        return User.model_validate(
            self.exec('SELECT * FROM user WHERE name = %s', (user.name,)).fetchone()
        )
    
    def get_settings(self, user: UserRead) -> UserSettings:
        return UserSettings.model_validate(
            self.exec('SELECT * FROM user_setting WHERE user_id = %s', (user.id,)).fetchone()
        )
    
    def update_settings(self, user: UserRead, settings: UserSettingsUpdate):
        settings_dict = settings.model_dump(exclude_none=True)
        sql = generate_update_sql('user_setting', settings_dict, 'user_id = %s')
        self.exec(sql, [*settings_dict.values(), user.id])