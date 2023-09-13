# from datetime import datetime
# from typing import Optional, List
# from sqlmodel import SQLModel, Field, Relationship
# from .user import User
# from .tag import Tag, AnimeTag
# from .category import Category, AnimeCategory

# # All required fields for creating record
# # Make it as base
# class AnimeBase(SQLModel):
#     name: str
    
# # Real table schema that will be created in database
# class Anime(AnimeBase, table=True):
#     id: int = Field(default=None, primary_key=True)
#     user: User = Relationship()
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     create_time: datetime = Field(default_factory=datetime.now)
#     watched_time: Optional[datetime]
#     downloaded: bool = Field(default=False)
#     watched: bool = Field(default=False)
#     rating: Optional[int]
#     comment: Optional[str]
#     url: Optional[str]
#     remark: Optional[str]
#     tmdb_id: Optional[str]
#     tags: List[Tag] = Relationship(link_model=AnimeTag)
#     categories: List[Category] = Relationship(link_model=AnimeCategory)

# # Alias for base, used for create new record
# class AnimeCreate(AnimeBase):
#     pass

schema = """
CREATE TABLE IF NOT EXISTS `anime` (
    `id` int(5) NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` int(5) NOT NULL,
    `name` varchar(100) NOT NULL,
    `added_time` DATETIME NOT NULL,
    `watched_time` DATETIME NOT NULL,
    `downloaded` BOOL NOT NULL DEFAULT FALSE,
    `watched` BOOL NOT NULL DEFAULT FALSE,
    `rating` int(3) NOT NULL DEFAULT 0,
    `comment` text DEFAULT NULL,
    `url` text DEFAULT NULL,
    `remark` text DEFAULT NULL,
    `tmdb_id` text DEFAULT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `name_uniq_id` (`user_id`,`name`)
) CHARACTER SET = utf8mb4;
"""