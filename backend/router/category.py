from fastapi import APIRouter, Depends
from typing import Annotated

# get /category/all get all categories
# get /category get category details
# get /category/anime get anime in this category
# post /category create category
# patch /category update category
# delete /category delete category

router = APIRouter(prefix='/category', tags=['category'])

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