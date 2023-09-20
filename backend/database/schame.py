user = """
CREATE TABLE IF NOT EXISTS `user` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` varchar(100) NOT NULL UNIQUE,
    `password` text NOT NULL
) CHARACTER SET = utf8mb4;
"""
user_setting = """
CREATE TABLE IF NOT EXISTS `user_setting` (
    `user_id` int NOT NULL PRIMARY KEY,
    `title` text NOT NULL,
    `title_watched` text NOT NULL,
    `title_unwatched` text NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE
) CHARACTER SET = utf8mb4;
"""
anime = """
CREATE TABLE IF NOT EXISTS `anime` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `added_time` DATETIME NOT NULL,
    `watched_time` DATETIME DEFAULT NULL,
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
tag = """
CREATE TABLE IF NOT EXISTS `tag` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `color` text DEFAULT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `name_uniq_id` (`user_id`,`name`)
)
"""
anime_tag = """
CREATE TABLE IF NOT EXISTS `anime_tag` (
    `user_id` int NOT NULL,
    `tag_id` int NOT NULL,
    `anime_id` int NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`tag_id`) REFERENCES `tag`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`anime_id`) REFERENCES `anime`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `anime_tag_uniq_id` (`tag_id`,`anime_id`)
)
"""
category = """
CREATE TABLE IF NOT EXISTS `category` (
    `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `color` text DEFAULT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `name_uniq_id` (`user_id`,`name`)
)
"""
anime_category = """
CREATE TABLE IF NOT EXISTS `anime_category` (
    `user_id` int NOT NULL,
    `category_id` int NOT NULL,
    `anime_id` int NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `user`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`category_id`) REFERENCES `category`(`id`) ON DELETE CASCADE,
    FOREIGN KEY(`anime_id`) REFERENCES `anime`(`id`) ON DELETE CASCADE,
    UNIQUE KEY `anime_tag_uniq_id` (`category_id`,`anime_id`)
)
"""

# Follow list order to create tables
schemas = [user, user_setting, anime, tag, anime_tag, category, anime_category]