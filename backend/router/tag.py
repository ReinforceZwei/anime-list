from fastapi import APIRouter, Depends, Path, Response
from typing import Annotated, List

from dal.tag import TagDao
from dal.anime_tag import AnimeTagDao
from model.tag import TagCreate, Tag, TagUpdate
from model.user import User
from model.anime import Anime
from dependencies import tag_dao, anime_tag_dao, get_current_user
from core.errors import DataNotFoundException

# get /tag/all get all tags
# get /tag get tag details
# get /tag/anime get anime with this tag
# post /tag create tag
# patch /tag update tag
# delete /tag delete tag

router = APIRouter(prefix='/tag', tags=['tag'])

@router.get('/all', response_model=List[Tag])
def get_all(tag_dao: Annotated[TagDao, Depends(tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    return tag_dao.get_all(user.id)

@router.post('/create', response_model=Tag)
def create(tag: TagCreate, tag_dao: Annotated[TagDao, Depends(tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    return tag_dao.create(user.id, tag.name, tag.color)

@router.get('/{id}', response_model=Tag)
def get(id: Annotated[int, Path()], tag_dao: Annotated[TagDao, Depends(tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    return tag_dao.get(user.id, id)

@router.get('/{id}/anime', response_model=List[Anime])
def get_anime(
    id: Annotated[int, Path()], tag_dao: Annotated[TagDao, Depends(tag_dao)], 
    anime_tag_dao: Annotated[AnimeTagDao, Depends(anime_tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    if not tag_dao.exists(id):
        raise DataNotFoundException()
    return anime_tag_dao.get_anime_by_tag(user.id, id)

@router.patch('/{id}', response_class=Response)
def update(id: Annotated[int, Path()], tag: TagUpdate, tag_dao: Annotated[TagDao, Depends(tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    tag_dao.update(user.id, id, tag)

@router.delete('/{id}', response_class=Response)
def delete(id: Annotated[int, Path()], tag_dao: Annotated[TagDao, Depends(tag_dao)], user: Annotated[User, Depends(get_current_user)]):
    tag_dao.delete(user.id, id)