import dataclasses
import jwt
import secrets
from model import Anime, User, AnimeModel, UserModel
from utils import timestamp, days_to_seconds
from log import logger

class AnimeController:
    """Controller provide abstract functions and input checking for interacting between user request and model functions"""
    def __init__(self, anime_model: AnimeModel) -> None:
        self._anime = anime_model
    
    def get(self, user_id: int, id: int) -> Anime | None:
        return self._anime.get(user_id, id)
    
    def get_all(self, user_id: int) -> list[Anime]:
        return self._anime.get_all(user_id)
    
    def add(self, user_id: int, name: str) -> Anime | None:
        return self._anime.add(user_id, name)
    
    def update(self, user_id: int, id: int, values: dict[str]) -> bool:
        filter_field = ['id', 'user_id']
        fields_type = {x.name: x.type for x in dataclasses.fields(Anime) if x.name not in filter_field}
        _values = {}
        for k, v in values.items():
            key_type = fields_type.get(k)
            if key_type is not None:
                match key_type:
                    case int() | bool():
                        _values[k] = int(v)
                    case _:
                        _values[k] = v

        return self._anime.update(user_id, id, _values)
    
    def last_modify(self, user_id: int) -> int:
        return self._anime.last_modify(user_id)

class UserController:
    def __init__(self, user_model: UserModel) -> None:
        self._user = user_model
        self._jwt_key = 'fixed_key' #secrets.token_urlsafe(16)
    
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
    
    def verify_token(self, jwt_token: str) -> int | None:
        """Verify user token. Return user ID if token vaild"""
        if len(jwt_token) == 0:
            return False
        try:
            payload = jwt.decode(jwt_token, self._jwt_key, ['HS256'])
            return payload['user_id']
        except jwt.exceptions.InvalidTokenError:
            logger.debug('verify_token token invalid', exc_info=1)
            return None

    def _generate_access_token(self, user: User) -> str:
        jwt_payload = {
            'user_id': user.user_id,
            'name': user.name,
            'sub': 'access',
            'iat': timestamp(),
            'exp': timestamp()+days_to_seconds(14)
        }
        return jwt.encode(jwt_payload, self._jwt_key, algorithm='HS256')

    def _generate_refresh_token(self, user: User) -> str:
        jwt_payload = {
            'user_id': user.user_id,
            'name': user.name,
            'sub': 'refresh',
            'iat': timestamp(),
            'exp': timestamp()+days_to_seconds(30)
        }
        return jwt.encode(jwt_payload, self._jwt_key, algorithm='HS256')
    
    def refresh_token(self, jwt_token: str) -> tuple[str, str] | None:
        """Refresh access token using a refresh token"""
        if len(jwt_token) == 0:
            return None
        try:
            # jwt library will handle exp and raise error
            payload = jwt.decode(jwt_token, self._jwt_key, ['HS256'])
            user = self._user.get(payload['user_id'])
            if user is not None:
                return (
                    self._generate_access_token(user),
                    self._generate_refresh_token(user)
                )
            else:
                return None
        except jwt.exceptions.InvalidTokenError:
            logger.debug('refresh_token token invalid', exc_info=1)
            return None
    
    def new_user(self, name: str, password: str) -> bool:
        if len(name) == 0 or len(name) > 100 or len(password) == 0:
            return False
        return self._user.add(name, password) is not None