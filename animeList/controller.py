import jwt
import secrets
from model import Anime, User, AnimeModel, UserModel
from utils import timestamp, days_to_seconds

class AnimeController:
    """Controller provide abstract functions and input checking for interacting between user request and model functions"""
    def __init__(self, anime_model: AnimeModel) -> None:
        self._anime = anime_model

class UserController:
    def __init__(self, user_model: UserModel) -> None:
        self._user = user_model
        self._jwt_key = secrets.token_urlsafe(16)
    
    def authenticate(self, name: str, password: str) -> tuple[str, str] | None:
        """Authenticate a user and return tuple of `(access token, refresh token)`"""
        if len(name) == 0 or len(password) == 0:
            return None
        if self._user.verify(name, password):
            user = self._user.get_by_name(name)
            return (
                self._generate_access_token(user),
                self._generate_refresh_token(user)
            )
        else:
            return None
    
    def _generate_access_token(self, user: User) -> str:
        jwt_payload = {
            'user_id': user.user_id,
            'name': user.name,
            'sub': 'access',
            'iat': timestamp(),
            'exp': timestamp()+days_to_seconds(14)
        }
        return jwt.encode(jwt_payload, self._jwt_key)

    def _generate_refresh_token(self, user: User) -> str:
        jwt_payload = {
            'user_id': user.user_id,
            'name': user.name,
            'sub': 'refresh',
            'iat': timestamp(),
            'exp': timestamp()+days_to_seconds(30)
        }
        return jwt.encode(jwt_payload, self._jwt_key)
    
    def refresh_token(self, jwt_token: str) -> tuple[str, str] | None:
        """Refresh access token using a refresh token"""
        if len(jwt_token) == 0:
            return None
        try:
            # jwt library will handle exp and raise error
            payload = jwt.decode(jwt_token, self._jwt_key, ['ES256'])
            user = self._user.get(payload['user_id'])
            if user is not None:
                return (
                    self._generate_access_token(user),
                    self._generate_refresh_token(user)
                )
            else:
                return None
        except jwt.exceptions.InvalidTokenError:
            return None