from dataclasses import dataclass
from database import AnimeDatabase
from log import logger
from utils import set_password, verify_password
import json
import pymysql.cursors

@dataclass
class User:
    user_id: int
    name: str
    password: str

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
    def __init__(self, database: AnimeDatabase) -> None:
        self._con = database.get_connection()

    def _execute(self, query: str, args=None) -> dict | tuple:
        c = self._con.cursor()
        try:
            rows = c.execute(query, args)
            result = c.fetchall()
            c.close()
            return result
        except pymysql.err.Error as e:
            c.close()
            logger.debug("Query error, "+str(e))
            return None

class AnimeModel(Model):
    """This class provide functions for communicating with database"""
    
    def add(self, user_id: int, name: str) -> bool:
        sql = "INSERT INTO anime(name, user_id) VALUES (%s, %s)"
        return self._execute(sql, (name, user_id)) is not None
    
    def update(self, user_id: int, id: int, values: dict) -> bool:
        pass
    
    def delete(self, user_id: int, id: int) -> bool:
        pass
    
    def get(self, user_id: int, id: int) -> Anime:
        pass
    
    def get_all(self, user_id: int) -> list[Anime]:
        pass
    
    def last_modify(self, user_id: int) -> int:
        pass

class UserModel(Model):
    """This class provide functions for user related data"""

    def get(self, user_id: int) -> User | None:
        sql = "SELECT * FROM user WHERE id = %s"
        result = self._execute(sql, (user_id,))
        if result and len(result) == 1:
            result = result[0]
            return User(result['id'], result['name'], result['password'])
        else: 
            return None
    
    def get_by_name(self, name: str) -> User | None:
        sql = "SELECT * FROM user WHERE name = %s"
        result = self._execute(sql, (name,))
        if result and len(result) == 1:
            result = result[0]
            return User(result['id'], result['name'], result['password'])
        else:
            return None
    
    def verify(self, name: str, password: str) -> bool:
        user = self.get_by_name(name)
        if user is not None:
            return verify_password(password, user.password)
        else:
            return False

    def add(self, name: str, password: str) -> User | None:
        sql = "INSERT INTO user(name, password) VALUES(%s, %s)"
        pwhash = set_password(password)
        if self._execute(sql, (name, pwhash)) is not None:
            user_id = self._con.insert_id()
            return User(user_id, name, pwhash)
        else:
            return None
    
    def delete(self, user_id: int) -> bool:
        sql = "DELETE FROM user WHERE id = %s"
        return self._execute(sql, (user_id,)) is not None