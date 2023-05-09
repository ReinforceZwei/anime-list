import os
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

@dataclass
class AppConfig:
    debug: bool
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    port: int
    secret_key: str
    app_name: str
    prefix_path: str
    
    @staticmethod
    def from_default():
        return AppConfig(
            debug = False,
            db_host = "",
            db_port = 3306,
            db_user = "",
            db_password = "",
            db_name = "animelist",
            port = 5000,
            secret_key = "",
            app_name = "Anime List",
            prefix_path = "",
        )
    
    @staticmethod
    def from_env():
        load_dotenv()
        return AppConfig(
            debug = os.getenv("DEBUG", False),
            db_host = os.getenv("DB_HOST", ""),
            db_port = int(os.getenv("DB_PORT", 3306)),
            db_user = os.getenv("DB_USER", ""),
            db_password = os.getenv("DB_PASSWORD", ""),
            db_name = os.getenv("DB_NAME", "animelist"),
            port = os.getenv("PORT", 5000),
            secret_key = os.getenv("SECRET_KEY", ""),
            app_name = os.getenv("APP_NAME", "Anime List"),
            prefix_path = os.getenv("PREFIX_PATH", "")
        )

    @staticmethod
    def load() -> type['AppConfig']:
        """Load config from dotenv file, env and app default"""
        return AppConfig(**{
            **asdict(AppConfig.from_default()),
            **asdict(AppConfig.from_env()),
        })