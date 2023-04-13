from dataclasses import dataclass
import json
import pymysql.cursors

@dataclass
class User:
    user_id: int
    name: str

@dataclass
class Anime:
    name: str
    id: int
    user_id: int
    added_time: int
    watched_time: int
    downloaded: bool
    watched: bool
    rating: int
    comment: str
    url: str
    remark: str
    tags: str

    def to_client_json(self) -> str:
        """Return a client compatiable json"""
        return json.dumps(self.to_client_dict())
    
    def to_client_dict(self) -> dict:
        """Return a client compatiable python dict"""
        _tag = "[]" if not self.tags else self.tags
        return {
            "name": self.name,
            "id": self.id,
            "addedTime": self.added_time,
            "watchedTime": self.watched_time,
            "downloaded": 1 if self.downloaded else 0,
            "watched": 1 if self.watched else 0,
            "rating": self.rating,
            "comment": self.comment,
            "url": self.url,
            "remark": self.remark,
            "tags": json.loads(_tag),
        }

class Model:
    def __init__(self, host, user, password, dbname) -> None:
        self._con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )

class AnimeModel(Model):
    """This class provide functions for communicating with database"""
    
    def add(self, user_id: int, name: str) -> bool:
        pass
    
    def update(self, user_id: int, id: int, values: dict) -> bool:
        pass
    
    def delete(self, user_id: int, id: int) -> bool:
        pass
    
    def get(self, user_id: int, id: int) -> Anime:
        pass
    
    def get_all(self, user_id: int) -> List[Anime]:
        pass
    
    def last_modify(self, user_id: int) -> int:
        pass

class UserModel(Model):
    """This class provide functions for user related data"""

    def get(self, user_id: int) -> User:
        pass
    
    def verify(self, name: str, password: str) -> bool:
        pass