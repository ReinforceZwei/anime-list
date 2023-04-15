from model import Anime, AnimeModel

class AnimeController:
    """Controller provide abstract functions and input checking for interacting between user request and model functions"""
    def __init__(self, anime_model: AnimeModel) -> None:
        self._anime = anime_model