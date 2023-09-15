from database.connection import PooledMySQLConnection
from mysql.connector.cursor import MySQLCursorDict

class BaseDao:
    def __init__(self, db: PooledMySQLConnection):
        self._db = db
        self._cur = self._db.cursor(dictionary=True)
    
    def exec(self, sql, params) -> MySQLCursorDict:
        self._cur.execute(sql, params)
        return self._cur