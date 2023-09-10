from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    debug: bool = False
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "rootpass"
    db_name: str = "animelist"
    port: int = 5000
    secret_key: str = "ChangeMe!"
    app_name: str = "Anime List"
    prefix_path: Optional[str]
    allow_register: bool = False

    default_title: str = "我的動漫列表"
    default_watched_title: str = "已看"
    default_unwatched_title: str = "想看"

    class Config:
        env_file = '.env'

settings = Settings()