from fastapi import Depends
from typing import Annotated, Dict, List

from database.connection import PooledMySQLConnection

from .base import BaseDao
from database.connection import PooledMySQLConnection
from model.anime import Anime, AnimeCreate, AnimeRead, AnimeUpdate
from model.user import User
from model.tag import Tag
from model.category import Category
from dal.tag import TagDao
from dal.category import CategoryDao
from dal.anime_tag import AnimeTagDao
from dal.anime_category import AnimeCategoryDao 
from core.utils import generate_update_sql

class AnimeDao(BaseDao):
    def __init__(
        self, db: PooledMySQLConnection,
        tag_dao: TagDao,
        category_dao: CategoryDao,
        anime_tag_dao: AnimeTagDao,
        anime_category_dao: AnimeCategoryDao
    ):
        super().__init__(db)
        self._tag_dao = tag_dao
        self._category_dao = category_dao
        self._anime_tag_dao = anime_tag_dao
        self._anime_category_dao = anime_category_dao
    
    def create(self, user_id: int, name: str) -> Anime:
        id = self.exec('INSERT INTO anime(name, user_id, added_time) VALUES (%s, %s, NOW())', (name, user_id)).lastrowid
        return self.get(user_id, id)
    
    def exists(self, id: int) -> bool:
        return self.row_exist('anime', 'id = %s', (id,))
    
    def get(self, user_id: int, anime_id: int) -> Anime:
        # TODO: Also fetch tags and categories
        anime = Anime.model_validate(
            self.exec('SELECT * FROM anime WHERE user_id = %s AND id = %s', (user_id, anime_id)).fetchone()
        )
        anime.tags = self._anime_tag_dao.get_tag_by_anime(user_id, anime.id)
        anime.category = self._anime_category_dao.get_category_by_anime(user_id, anime.id)
        return anime
    
    def get_all(self, user_id: int) -> List[Anime]:
        tags: Dict[int, List[int]] = dict()
        for tag_link in self._anime_tag_dao.get_all_link(user_id):
            tags.setdefault(tag_link['anime_id'], []).append(int(tag_link['tag_id']))
        
        categories: Dict[int, List[int]] = dict()
        for category_link in self._anime_category_dao.get_all_link(user_id):
            categories.setdefault(category_link['anime_id'], []).append(category_link['category_id'])

        animes: List[Anime] = []
        for anime in self.exec('SELECT * FROM anime WHERE user_id = %s', (user_id,)).fetchall():
            anime_model = Anime.model_validate(anime)
            if anime_model.id in tags:
                anime_model.tags = tags[anime_model.id]
            if anime_model.id in categories:
                anime_model.category = categories[anime_model.id]
            animes.append(anime_model)
        return animes
    
    def update(self, user_id: int, anime_id: int, anime: AnimeUpdate):
        anime_dict = anime.model_dump(exclude_none=True, exclude={'id'})
        sql = generate_update_sql('anime', anime_dict, 'user_id = %s AND id = %s')
        self.exec(sql, [*anime_dict, user_id, anime.id])
    
    def delete(self, user_id: int, anime_id: int):
        self.exec('DELETE FROM anime WHERE user_id = %s AND id = %s', (user_id, anime_id)).rowcount