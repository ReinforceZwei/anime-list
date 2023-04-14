from log import logger
import pymysql.cursors

# Cannot execute multiple query once. Split them into list
DB_SCHEMA = ["""
CREATE TABLE IF NOT EXISTS `user` (
    `id` int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `password` text NOT NULL
) CHARACTER SET = utf8mb4;
""", """
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
) CHARACTER SET = utf8mb4;
"""]

class AnimeDatabase:
    """This class initialize database for this application to use"""

    def __init__(self, host, user, password, dbname, port = 3306) -> None:
        self._con = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self._dbname = dbname
        self._init_schema()
    
    def _init_schema(self):
        logger.debug("Prepare database")
        self._con.query("CREATE DATABASE IF NOT EXISTS `{}` CHARACTER SET utf8mb4".format(self._dbname))
        self._con.select_db(self._dbname)
        for table in DB_SCHEMA:
            self._con.query(table)
        logger.debug("Done")

    def get_connection(self) -> type['pymysql.Connection[pymysql.cursors.DictCursor]']:
        return self._con
