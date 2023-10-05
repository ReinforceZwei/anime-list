from typing import List
from .base import BaseDao
from model.anime import Anime
from model.category import Category

class AnimeCategoryDao(BaseDao):
    def get_anime_by_category(self, user_id: int, category_id: int) -> List[Anime]:
        sql = 'SELECT * FROM anime_category JOIN anime ON anime_category.anime_id = anime.id WHERE anime_category.category_id = %s AND anime_category.user_id = %s'
        animes = self.exec(sql, (category_id, user_id)).fetchall()
        result = [Anime.model_validate(anime) for anime in animes]
        return result
    
    def get_category_by_anime(self, user_id: int, anime_id: int) -> List[Category]:
        sql = 'SELECT * FROM anime_category JOIN category ON anime_category.category_id = category.id WHERE anime_category.anime_id = %s AND anime_category.user_id = %s'
        categorys = self.exec(sql, (anime_id, user_id)).fetchall()
        result = [Category.model_validate(category) for category in categorys]
        return result
    
    def get_all_link(self, user_id: int):
        sql = 'SELECT * FROM anime_category WHERE user_id = %s'
        return self.exec(sql, (user_id,)).fetchall()
    
    def create_link(self, user_id: int, category_id: int, anime_id: int):
        sql = 'INSERT INTO anime_category VALUES (%s, %s, %s)'
        self.exec(sql, (user_id, category_id, anime_id)).rowcount
    
    def delete_link(self, user_id: int, category_id: int, anime_id: int):
        sql = 'DELETE FROM anime_category WHERE category_id = %s AND anime_id = %s AND user_id = %s'
        self.exec(sql, (category_id, anime_id, user_id)).rowcount