from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session

from dal.user import UserDao
from model.user import UserLogin, UserRead, UserSettings
from database.schema.user import User
from dependencies import db_session, user_dao


router = APIRouter(prefix='/user')

@router.post('/login')
def login(user: UserLogin, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.login(user)

@router.post('/create')
def create(user: User, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.create(user)

@router.get('/get')
def get(user: UserRead, user_dao: Annotated[UserDao, Depends(user_dao)]):
    return user_dao.get(user)

@router.get('/settings', response_model=UserSettings)
def get_settings(user: UserRead):
    return UserSettings()