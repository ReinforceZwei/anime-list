import pymysql.cursors

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS `user` (
  `id` int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `password` text NOT NULL
)

CREATE TABLE IF NOT EXISTS `anime` (
  `name` varchar(100) NOT NULL,
  `id` int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  `user_id` int(5) NOT NULL,
  `added_time` int(10) DEFAULT 0,
  `watched_time` int(10) NOT NULL DEFAULT 0,
  `downloaded` tinyint(1) NOT NULL DEFAULT 0,
  `watched` tinyint(1) NOT NULL DEFAULT 0,
  `rating` int(1) NOT NULL DEFAULT 0,
  `comment` text DEFAULT NULL,
  `url` text DEFAULT NULL,
  `remark` varchar(500) DEFAULT NULL,
  `tags` varchar(1000) NOT NULL DEFAULT '[]',
  FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
)
"""

class AnimeDatabase:
    """This class initialize database for this application to use"""

    def __init__(self, host, user, password, dbname, port = 3306) -> None:
        self._con = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            cursorclass=pymysql.cursors.DictCursor
        )
        self._init_schema()
    
    def _init_schema(self):
        with self._con.cursor() as cursor:
            cursor.executemany(DB_SCHEMA)
        self._con.commit()

    def get_connection(self) -> type['pymysql.Connection[pymysql.cursors.DictCursor]']:
        return self._con
