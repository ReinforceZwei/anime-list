import mysql.connector
from mysql.connector import errorcode
from .schame import schemas
from core.config import settings
from .connection import get_connection, set_database

con = get_connection()
cursor = con.cursor()

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS `{}` CHARACTER SET utf8mb4".format(settings.db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE `{}`".format(settings.db_name))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(settings.db_name))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(settings.db_name))
        con.database = settings.db_name
        cursor.execute("USE `{}`".format(settings.db_name))
    else:
        print(err)
        exit(1)

set_database(settings.db_name)

for s in schemas:
    cursor.execute(s)

cursor.close()
con.close()

print('Database ready')
