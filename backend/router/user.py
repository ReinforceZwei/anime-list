from fastapi import APIRouter, Depends, HTTPException, Path
from typing import Annotated

from pydantic import ValidationError

from dal.user import UserDao
from model.user import User, UserLogin, UserRead, UserSettings, UserTokenPair, UserRefresh, UserInfo, UserSettingsUpdate
from dependencies import user_dao, get_current_user
from core.utils import set_password, verify_password, generate_access_token, generate_refresh_token, decode_user_token_no_verify, decode_user_token
from core.config import settings

# get /user get user details
# post /user create new user
# post /user/login login user
# get /user/settings get user settings
# patch /user/settings update user settings

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/details', response_model=UserInfo)
def get(user: Annotated[User, Depends(get_current_user)], user_dao: Annotated[UserDao, Depends(user_dao)]):
    return UserInfo.model_validate(user_dao.get(user.id).model_dump())

@router.post('/create', response_model=UserInfo)
def create(user: UserLogin, user_dao: Annotated[UserDao, Depends(user_dao)]):
    user.password = set_password(user.password)
    db_user = user_dao.create(user.name, user.password)
    return UserInfo(id=db_user.id, name=db_user.name)

@router.post('/login', response_model=UserTokenPair)
def login(user: UserLogin, user_dao: Annotated[UserDao, Depends(user_dao)]):
    if (db_user := user_dao.get_by_name(user.name)) is not None:
        if verify_password(user.password, db_user.password):
            # Ok
            return UserTokenPair(
                token=generate_access_token(settings.secret_key, db_user.id, db_user.name, db_user.password),
                refresh_token=generate_refresh_token(settings.secret_key, db_user.id, db_user.name, db_user.password)
            )
        else:
            raise HTTPException(401, "Incorrect password")
    else:
        raise HTTPException(401, "Incorrect user")

@router.post('/refresh')
def refresh(user: UserRefresh, user_dao: Annotated[UserDao, Depends(user_dao)]):
    error_unauthorized = HTTPException(401, "Unauthorized")
    try:
        # Need to fetch user password from DB to verify JWT signature
        jwt_payload = decode_user_token_no_verify(user.refresh_token)
        if jwt_payload['sub'] != 'refresh':
            raise error_unauthorized
        unsafe_user = UserInfo.model_validate(jwt_payload)
        db_user = user_dao.get(unsafe_user.id)
        if db_user.name == unsafe_user.name:
            # Verify JWT using user password
            decode_user_token(settings.secret_key, db_user.password, user.refresh_token)
            # No error then issue new token pair
            return UserTokenPair(
                token=generate_access_token(settings.secret_key, db_user.id, db_user.name, db_user.password),
                refresh_token=generate_refresh_token(settings.secret_key, db_user.id, db_user.name, db_user.password)
            )
    except HTTPException:
        pass
    except ValidationError as e:
        print(e)
        raise error_unauthorized
    except Exception:
        raise error_unauthorized

@router.get('/settings', response_model=UserSettings)
def get_settings(user: Annotated[User, Depends(get_current_user)], user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.get_settings(user.id)

@router.patch('/settings')
def update_settings(update_settings: UserSettingsUpdate, user: Annotated[User, Depends(get_current_user)], user_dao: Annotated[UserDao, Depends(user_dao)]):
    user_dao.update_settings(user.id, update_settings)