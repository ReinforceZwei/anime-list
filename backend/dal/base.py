from mysql.connector.cursor import MySQLCursorDict

from database.connection import PooledMySQLConnection
from core.errors import DataNotFoundException

class CursorWrapper:
    def __init__(self, cursor: MySQLCursorDict):
        self._cur = cursor
    
    def fetchone(self):
        result = self._cur.fetchone()
        if result is not None:
            return result
        else:
            raise DataNotFoundException("No data found")
    
    def fetchall(self):
        result = self._cur.fetchall()
        return result
    
    @property
    def lastrowid(self):
        row_id = self._cur.lastrowid
        if row_id is not None:
            return row_id
        else:
            raise DataNotFoundException("No last row ID available")

class BaseDao:
    def __init__(self, db: PooledMySQLConnection):
        self._db = db
        self._cur = self._db.cursor(dictionary=True)
    
    def exec(self, sql, params) -> CursorWrapper:
        self._cur.execute(sql, params)
        return CursorWrapper(self._cur)