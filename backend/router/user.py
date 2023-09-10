from fastapi import APIRouter
from schema.user import UserCreate, UserRead, UserSettings

router = APIRouter(prefix='/user')

@router.post('/login')
def login(user: UserCreate):
    return user

@router.get('/settings', response_model=UserSettings)
def get_settings(user: UserRead):
    return UserSettings()