from typing import List
from .base import BaseDao
from model.anime import Anime
from model.tag import Tag

class AnimeTagDao(BaseDao):
    def get_anime_by_tag(self, user_id: int, tag_id: int) -> List[Anime]:
        sql = 'SELECT * FROM anime_tag JOIN anime ON anime_tag.anime_id = anime.id WHERE anime_tag.tag_id = %s AND anime_tag.user_id = %s'
        animes = self.exec(sql, (tag_id, user_id)).fetchall()
        result = [Anime.model_validate(anime) for anime in animes]
        return result
    
    def get_tag_by_anime(self, user_id: int, anime_id: int) -> List[Tag]:
        sql = 'SELECT * FROM anime_tag JOIN tag ON anime_tag.tag_id = tag.id WHERE anime_tag.anime_id = %s AND anime_tag.user_id = %s'
        tags = self.exec(sql, (anime_id, user_id)).fetchall()
        result = [Tag.model_validate(tag) for tag in tags]
        return result
    
    def get_all_link(self, user_id: int):
        sql = 'SELECT * FROM anime_tag WHERE user_id = %s'
        return self.exec(sql, (user_id,)).fetchall()
    
    def create_link(self, user_id: int, tag_id: int, anime_id: int):
        sql = 'INSERT INTO anime_tag VALUES (%s, %s, %s)'
        self.exec(sql, (user_id, tag_id, anime_id)).rowcount
    
    def delete_link(self, user_id: int, tag_id: int, anime_id: int):
        sql = 'DELETE FROM anime_tag WHERE tag_id = %s AND anime_id = %s AND user_id = %s'
        self.exec(sql, (tag_id, anime_id, user_id)).rowcount