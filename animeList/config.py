import os
from dataclasses import dataclass, asdict
from dotenv import load_dotenv

@dataclass
class AppConfig:
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    port: int
    
    @staticmethod
    def from_default():
        return AppConfig(
            db_host = "",
            db_port = 3306,
            db_user = "",
            db_password = "",
            db_name = "animelist",
            port = 5000,
        )
    
    @staticmethod
    def from_env():
        load_dotenv()
        return AppConfig(
            db_host = os.getenv("DB_HOST", ""),
            db_port = int(os.getenv("DB_PORT", 3306)),
            db_user = os.getenv("DB_USER", ""),
            db_password = os.getenv("DB_PASSWORD", ""),
            db_name = os.getenv("DB_NAME", "animelist"),
            port = os.getenv("PORT", 5000)
        )

    @staticmethod
    def load() -> type['AppConfig']:
        """Load config from dotenv file, env and app default"""
        return AppConfig(**{
            **asdict(AppConfig.from_default()),
            **asdict(AppConfig.from_env()),
        })