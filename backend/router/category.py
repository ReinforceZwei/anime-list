from fastapi import APIRouter, Depends, Path, Response
from typing import Annotated, List

from dal.category import CategoryDao
from dal.anime_category import AnimeCategoryDao
from model.anime import Anime
from model.category import Category, CategoryUpdate, CategoryCreate
from model.user import User
from dependencies import category_dao, anime_category_dao, get_current_user
from core.errors import DataNotFoundException

# get /category/all get all categories
# get /category get category details
# get /category/anime get anime in this category
# post /category create category
# patch /category update category
# delete /category delete category

router = APIRouter(prefix='/category', tags=['category'])

@router.get('/all', response_model=List[Category])
def get_all(
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    return category_dao.get_all(user.id)

@router.post('/create', response_model=Category)
def create(
    category: CategoryCreate,
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    return category_dao.create(user.id, category.name, category.color)

@router.get('/{id}', response_model=Category)
def get(
    id: Annotated[int, Path()],
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    return category_dao.get(user.id, id)

@router.get('/{id}/anime', response_model=List[Anime])
def get_anime(
    id: Annotated[int, Path()],
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    anime_category_dao: Annotated[AnimeCategoryDao, Depends(anime_category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    if not category_dao.exists(id):
        raise DataNotFoundException()
    return anime_category_dao.get_anime_by_category(user.id, id)

@router.patch('/{id}', response_class=Response)
def update(
    id: Annotated[int, Path()],
    category: CategoryUpdate,
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    category_dao.update(user.id, id, category)

@router.delete('/{id}', response_class=Response)
def delete(
    id: Annotated[int, Path()],
    category_dao: Annotated[CategoryDao, Depends(category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    category_dao.delete(user.id, id)