import dataclasses
from dataclasses import dataclass
from database import AnimeDatabase
from log import logger
from utils import set_password, verify_password, timestamp
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
            "animeName": self.name,
            "animeID": self.id,
            "addedTime": self.added_time,
            "watchedTime": self.watched_time,
            "downloaded": 1 if self.downloaded else 0,
            "watched": 1 if self.watched else 0,
            "rating": self.rating,
            "comment": self.comment if not None else '',
            "url": self.url if not None else '',
            "remark": self.remark if not None else '',
            "tags": json.loads(_tag),
        }

class Model:
    def __init__(self, database: AnimeDatabase) -> None:
        self._con = database.get_connection()

    def _execute(self, query: str, args=None) -> dict | tuple:
        c = self._con.cursor()
        try:
            logger.debug("Execute query '%s', %s", query, args)
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
    
    def add(self, user_id: int, name: str) -> Anime | None:
        sql = "INSERT INTO anime(name, user_id, added_time) VALUES (%s, %s, %s)"
        result = self._execute(sql, (name, user_id, timestamp()))
        if result is not None:
            id = self._con.insert_id()
            self._update_last_modify(user_id)
            return self.get(user_id, id)
        else:
            return None
    
    def update(self, user_id: int, id: int, values: dict[str]) -> bool:
        # Get available fields from Anime class
        filter_field = ['id', 'user_id']
        fields_name = [x.name for x in dataclasses.fields(Anime) if x.name not in filter_field]
        fields_type = {x.name: x.type for x in dataclasses.fields(Anime) if x.name not in filter_field}
        # Filter out vaild fields by name
        to_update = {k: v for k, v in values.items() if k in fields_name}.items()
        if not to_update:
            return False
        
        self._update_last_modify(user_id)

        field_sql = []
        for k, v in to_update:
            k_type = fields_type.get(k)
            if k_type is str:
                v = self._con.escape_string(v)
                field_sql.append("{} = '{}'".format(k, v))
            else:
                field_sql.append("{} = {}".format(k, v))

        field_sql = ", ".join(field_sql)
        sql = "UPDATE anime SET {field} WHERE user_id = %s AND id = %s".format(field = field_sql)
        return self._execute(sql, (user_id, id)) is not None
    
    def delete(self, user_id: int, id: int) -> bool:
        self._update_last_modify(user_id)

        sql = "DELETE FROM anime WHERE user_id = %s AND id = %s"
        return self._execute(sql, (user_id, id)) is not None
    
    def get(self, user_id: int, id: int) -> Anime | None:
        sql = "SELECT * FROM anime WHERE user_id = %s AND id = %s"
        result = self._execute(sql, (user_id, id))
        if result and len(result) == 1:
            return Anime(**(result[0]))
        else:
            return None
    
    def get_all(self, user_id: int) -> list[Anime]:
        sql = "SELECT * FROM anime WHERE user_id = %s ORDER BY id"
        result = self._execute(sql, (user_id,))
        if result and len(result) > 0:
            return [Anime(**x) for x in result]
        else:
            return []
    
    def get_watched_sorted(self, user_id: int) -> list[Anime]:
        sql = "SELECT * FROM anime WHERE user_id = %s AND watched = 1 ORDER BY watched_time"
        result = self._execute(sql, (user_id,))
        if result and len(result) > 0:
            return [Anime(**x) for x in result]
        else:
            return []
    
    def get_unwatched_sorted(self, user_id: int) -> list[Anime]:
        sql = "SELECT * FROM anime WHERE user_id = %s AND watched = 0 ORDER BY watched_time"
        result = self._execute(sql, (user_id,))
        if result and len(result) > 0:
            return [Anime(**x) for x in result]
        else:
            return []

    def last_modify(self, user_id: int) -> int:
        sql = "SELECT time FROM last_modify WHERE user_id = %s"
        result = self._execute(sql, (user_id,))
        if result and len(result) == 1:
            return int(result[0]['time'])
        else:
            return 0
    
    def _update_last_modify(self, user_id: int) -> bool:
        sql = "INSERT INTO last_modify VALUES(%(user_id)s, %(time)s) ON DUPLICATE KEY UPDATE time = %(time)s"
        return self._execute(sql, {'time':timestamp(), 'user_id':user_id}) is not None

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