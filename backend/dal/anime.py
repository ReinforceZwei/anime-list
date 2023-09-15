from fastapi import Depends
from typing import Annotated

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.anime import Anime, AnimeCreate, AnimeRead
from model.user import User

class AnimeDao(BaseDao):
    def create(self, user: UserRead, anime: AnimeCreate):
        id = self.exec('INSERT INTO anime(name, user_id) VALUES (%s, %s)', (anime.name, user.id)).lastrowid
        return self.get(user, AnimeRead(id=id))
    
    def get(self, user: UserRead, anime: AnimeRead):
        return Anime.model_validate(
            self.exec('SELECT * FROM anime WHERE user_id = %s AND id = %s', (user.id, anime.id)).fetchone()
        )