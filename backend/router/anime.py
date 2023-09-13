from fastapi import APIRouter, Depends
from typing import Annotated


# get /anime get details
# post /anime create new anime
# patch /anime update anime
# delete /anime delete anime
# get /anime/tag get tags
# patch /anime/tag link tags to anime
# delete /anime/tag delete linked tags
# get /anime/category get category
# patch /anime/category link category to anime
# delete /anime/category delete linked category

router = APIRouter(prefix='/anime', tags=['anime'])

@router.get('/')
def get_anime():
    pass

@router.post('/')
def create_anime():
    pass

@router.patch('/')
def update_anime():
    pass

@router.delete('/')
def delete_anime():
    pass

@router.get('/tag')
def get_tag():
    pass

@router.patch('/tag')
def update_tag():
    pass

@router.delete('/tag')
def delete_tag():
    pass

@router.get('/category')
def get_category():
    pass

@router.patch('/category')
def update_category():
    pass

@router.delete('/category')
def delete_category():
    pass