from core.config import settings

import mysql.connector

con_pool = mysql.connector.pooling.MySQLConnectionPool(
    host=settings.db_host,
    user=settings.db_user,
    password=settings.db_password,
    port=settings.db_port,
    autocommit=True
)

def get_connection():
    return con_pool.get_connection()

def set_database(name):
    con_pool.set_config(database=name)