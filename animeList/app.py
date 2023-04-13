import flask
from config import AppConfig
from database import AnimeDatabase

config = AppConfig.Load()
print(config)
db = AnimeDatabase(
    host=config.db_host,
    user=config.db_user,
    password=config.db_password,
    dbname=config.db_name,
    port=config.db_port
)