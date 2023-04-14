import flask
from config import AppConfig
from database import AnimeDatabase
from model import AnimeModel, UserModel

config = AppConfig.load()
db = AnimeDatabase(
    host=config.db_host,
    user=config.db_user,
    password=config.db_password,
    dbname=config.db_name,
    port=config.db_port
)
anime = AnimeModel(db)
user = UserModel(db)