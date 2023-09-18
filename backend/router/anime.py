from fastapi import APIRouter, Depends, Path
from typing import Annotated
from model.anime import AnimeCreate

from dal.anime import AnimeDao
from dependencies import anime_dao

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

@router.post('/create')
def create_anime(anime: AnimeCreate, anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.get('/{id}')
def get_anime(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.patch('/{id}')
def update_anime(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.delete('/{id}')
def delete_anime(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.get('/{id}/tag')
def get_tag(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.patch('/{id}/tag')
def update_tag(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.delete('/{id}/tag')
def delete_tag(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.get('/{id}/category')
def get_category(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.patch('/{id}/category')
def update_category(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass

@router.delete('/{id}/category')
def delete_category(id: Annotated[int, Path()], anime_dao: Annotated[AnimeDao, Depends(anime_dao)]):
    pass