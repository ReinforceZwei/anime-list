from dataclasses import dataclass
import pymysql.cursors

@dataclass
class Anime:
    name: str
    id: int
    addedTime: int
    watchedTime: int
    downloaded: bool
    watched: bool
    rating: int
    comment: str
    url: str
    remark: str
    tags: str

class AnimeModel:
    """This class provide functions for communicating with database"""

    def __init__(self, host, user, password, dbname) -> None:
        self._con = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )