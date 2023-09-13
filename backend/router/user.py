from fastapi import APIRouter, Depends
from typing import Annotated

from dal.user import UserDao
from model.user import UserLogin, UserRead, UserSettings
from dependencies import db_session, user_dao

# get /user get user details
# post /user create new user
# post /user/login login user
# get /user/settings get user settings
# patch /user/settings update user settings

router = APIRouter(prefix='/user', tags=['user'])

@router.get('/')
def get(user: UserRead, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.get(user)

@router.post('/')
def create(user: UserLogin, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.create(user)

@router.post('/login')
def login(user: UserLogin, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.login(user)

@router.get('/settings', response_model=UserSettings)
def get_settings(user: UserRead):
    return UserSettings()

@router.patch('/settings')
def update_settings():
    pass