from fastapi import APIRouter, Depends
from typing import Annotated

# get /tag/all get all tags
# get /tag get tag details
# get /tag/anime get anime with this tag
# post /tag create tag
# patch /tag update tag
# delete /tag delete tag

router = APIRouter(prefix='/tag', tags=['tag'])

@router.get('/all')
def get_all():
    pass

@router.get('/')
def get():
    pass

@router.get('/anime')
def get_anime():
    pass

@router.post('/')
def create():
    pass

@router.patch('/')
def update():
    pass

@router.delete('/')
def delete():
    pass