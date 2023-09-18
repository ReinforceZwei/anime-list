from fastapi import Depends
from typing import Annotated

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.anime import Anime, AnimeCreate, AnimeRead, AnimeUpdate
from model.user import User
from core.utils import generate_update_sql

class AnimeDao(BaseDao):
    def create(self, user_id: int, name: str):
        id = self.exec('INSERT INTO anime(name, user_id, added_time) VALUES (%s, %s, NOW())', (name, user_id)).lastrowid
        return self.get(user_id, id)
    
    def get(self, user_id: int, anime_id: int):
        # TODO: Also fetch tags and categories
        return Anime.model_validate(
            self.exec('SELECT * FROM anime WHERE user_id = %s AND id = %s', (user_id, anime_id)).fetchone()
        )
    
    def update(self, user_id: int, anime_id: int, anime: AnimeUpdate):
        anime_dict = anime.model_dump(exclude_none=True, exclude={'id'})
        sql = generate_update_sql('anime', anime_dict, 'user_id = %s AND id = %s')
        self.exec(sql, [*anime_dict, user_id, anime.id])
    
    def delete(self, user_id: int, anime_id: int):
        self.exec('DELETE FROM anime WHERE user_id = %s AND id = %s', (user_id, anime_id))