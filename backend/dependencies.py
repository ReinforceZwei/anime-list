from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, HTTPBearer
import fastapi.security
from typing import Annotated, Any
from mysql import connector
import mysql.connector.errors as sql_error

from pydantic import ValidationError, errors
from core.config import settings
from core.utils import generate_access_token, generate_refresh_token
from model.user import User, UserRead, UserTokenPair, UserInfo

from database.connection import get_connection, PooledMySQLConnection
from dal.user import UserDao
from dal.anime import AnimeDao
from dal.tag import TagDao
from dal.anime_tag import AnimeTagDao
from dal.category import CategoryDao
from dal.anime_category import AnimeCategoryDao
from core.utils import decode_user_token_no_verify, decode_user_token
from core.errors import DataNotFoundException

oauth2_scheme = HTTPBearer()#OAuth2AuthorizationCodeBearer(tokenUrl="api/user/login", authorizationUrl="")

def get_bearer(token: Annotated[Any, Depends(oauth2_scheme)]) -> str:
    return token.credentials

def db_session() -> PooledMySQLConnection:
    db = get_connection()
    try:
        yield db
    except sql_error.IntegrityError:
        raise HTTPException(409, "Resource with same name already exist")
    finally:
        db.close()

def user_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return UserDao(db)

def tag_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return TagDao(db)

def anime_tag_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return AnimeTagDao(db)

def category_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return CategoryDao(db)

def anime_category_dao(db: Annotated[PooledMySQLConnection, Depends(db_session)]):
    return AnimeCategoryDao(db)

def anime_dao(
    db: Annotated[PooledMySQLConnection, Depends(db_session)],
    tag_dao: Annotated[TagDao, Depends(tag_dao)],
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    anime_tag_dao: Annotated[AnimeTagDao, Depends(anime_tag_dao)],
    anime_category_dao: Annotated[AnimeCategoryDao, Depends(anime_category_dao)]
):
    return AnimeDao(db, tag_dao, category_dao, anime_tag_dao, anime_category_dao)


def get_current_user(token: Annotated[str, Depends(get_bearer)], user_dao: Annotated[UserDao, Depends(user_dao)], request: Request) -> User:
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
            request.state.user = db_user
            return db_user
    except HTTPException:
        raise
    except ValidationError as e:
        raise HTTPException(401, e)
    except DataNotFoundException:
        raise error_unauthorized
    except Exception as e:
        raise HTTPException(401, e)