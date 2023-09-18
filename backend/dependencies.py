from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, HTTPBearer
import fastapi.security
from typing import Annotated, Any

from pydantic import ValidationError
from core.config import settings
from core.utils import generate_access_token, generate_refresh_token
from model.user import User, UserRead, UserTokenPair, UserInfo

from database.connection import get_connection, PooledMySQLConnection
from dal.user import UserDao
from dal.anime import AnimeDao
from core.utils import decode_user_token_no_verify, decode_user_token

oauth2_scheme = HTTPBearer()#OAuth2AuthorizationCodeBearer(tokenUrl="api/user/login", authorizationUrl="")

def get_bearer(token: Annotated[Any, Depends(oauth2_scheme)]) -> str:
    return token.credentials

def db_session() -> PooledMySQLConnection:
    db = get_connection()
    try:
        yield db
    finally:
        db.close()

def user_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return UserDao(db)

def anime_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return AnimeDao(db)

def get_current_user(token: Annotated[str, Depends(get_bearer)], user_dao: Annotated[UserDao, Depends(user_dao)]) -> User:
    error_unauthorized = HTTPException(401, "Unauthorized")
    try:
        jwt_payload = decode_user_token_no_verify(token)
        if jwt_payload['sub'] != 'access':
            raise error_unauthorized
        unsafe_user = UserInfo.model_validate(jwt_payload)
        db_user = user_dao.get(unsafe_user.id)
        if db_user.name == unsafe_user.name:
            # Verify JWT using user password
            decode_user_token(settings.secret_key, db_user.password, token)
            # No error then return user
            return db_user
    except HTTPException:
        raise
    except ValidationError as e:
        raise HTTPException(401, e)
    except Exception as e:
        raise HTTPException(401, e)