from typing import List
from .base import BaseDao
from model.tag import Tag, TagUpdate
from core.utils import generate_update_sql

class TagDao(BaseDao):
    def create(self, user_id: int, name: str, color: str = None) -> Tag:
        id = self.exec('INSERT INTO tag(user_id, name, color) VALUES (%s, %s, %s)', (user_id, name, color)).lastrowid
        return self.get(user_id, id)
    
    def exists(self, id: int) -> bool:
        return self.row_exist('tag', 'id = %s', (id,))
    
    def get(self, user_id: int, id: int) -> Tag:
        return Tag.model_validate(
            self.exec('SELECT * FROM tag WHERE user_id = %s AND id = %s', (user_id, id)).fetchone()
        )
    
    def get_all(self, user_id: int) -> List[Tag]:
        return [Tag.model_validate(tag) for tag in self.exec('SELECT * FROM tag WHERE user_id = %s', (user_id,)).fetchall()]
    
    def update(self, user_id: int, id: int, tag: TagUpdate):
        tag_dict = tag.model_dump(exclude_none=True)
        sql = generate_update_sql('tag', tag_dict, 'user_id = %s AND id = %s')
        self.exec(sql, [*tag_dict.values(), user_id, id])

    def delete(self, user_id: int, id: int):
        self.exec('DELETE FROM tag WHERE user_id = %s AND id = %s', (user_id, id)).rowcount