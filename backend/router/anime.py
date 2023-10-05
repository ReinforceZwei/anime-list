from fastapi import APIRouter, Depends, Path, Response
from typing import Annotated, List

from model.anime import Anime, AnimeCreate, AnimeUpdate
from model.user import User
from model.tag import Tag
from model.category import Category
from dal.anime import AnimeDao
from dal.anime_tag import AnimeTagDao
from dal.anime_category import AnimeCategoryDao
from dependencies import anime_dao, anime_tag_dao, anime_category_dao, get_current_user

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

router = APIRouter(prefix='/anime', tags=['anime'], dependencies=[Depends(get_current_user)])

@router.post('/create', response_model=Anime)
def create_anime(anime: AnimeCreate, anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    return anime_dao.create(user.id, anime.name)

@router.get('/all', response_model=List[Anime])
def get_all(anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    return anime_dao.get_all(user.id)

@router.get('/{id}', response_model=Anime)
def get_anime(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    return anime_dao.get(user.id, id)

@router.patch('/{id}', response_class=Response)
def update_anime(id: Annotated[int, Path()], anime: AnimeUpdate, anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    anime_dao.update(user.id, id, anime)
    return Response

@router.delete('/{id}', response_class=Response)
def delete_anime(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    anime_dao.delete(user.id, id)

@router.get('/{id}/tag', response_model=List[Tag])
def get_tag(
    id: Annotated[int, Path()], anime_tag_dao: Annotated[AnimeTagDao, Depends(anime_tag_dao)], 
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    return anime_tag_dao.get_tag_by_anime(user.id, id)

@router.post('/{id}/tag', response_class=Response)
def add_tag(
    id: Annotated[int, Path()], tag_ids: List[int], anime_tag_dao: Annotated[AnimeTagDao, Depends(anime_tag_dao)], 
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    for tag_id in tag_ids:
        anime_tag_dao.create_link(user.id, tag_id, id)

@router.delete('/{id}/tag', response_class=Response)
def delete_tag(
    id: Annotated[int, Path()], tag_ids: List[int], anime_tag_dao: Annotated[AnimeTagDao, Depends(anime_tag_dao)],
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)], user: Annotated[User, Depends(get_current_user)]):
    for tag_id in tag_ids:
        anime_tag_dao.delete_link(user.id, tag_id, id)

@router.get('/{id}/category', response_model=List[Category])
def get_category(
    id: Annotated[int, Path()],
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)],
    anime_category_dao: Annotated[AnimeCategoryDao, Depends(anime_category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    return anime_category_dao.get_category_by_anime(user.id, id)

@router.post('/{id}/category', response_class=Response)
def add_category(
    id: Annotated[int, Path()],
    category_ids: List[int],
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)],
    anime_category_dao: Annotated[AnimeCategoryDao, Depends(anime_category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    for category_id in category_ids:
        anime_category_dao.create_link(user.id, category_id, id)

@router.delete('/{id}/category', response_class=Response)
def delete_category(
    id: Annotated[int, Path()],
    category_ids: List[int],
    anime_dao: Annotated[AnimeDao, Depends(anime_dao)],
    anime_category_dao: Annotated[AnimeCategoryDao, Depends(anime_category_dao)],
    user: Annotated[User, Depends(get_current_user)]
):
    for category_id in category_ids:
        anime_category_dao.delete_link(user.id, category_id, id)