from typing import List
from .base import BaseDao
from model.category import Category, CategoryUpdate
from core.utils import generate_update_sql

class CategoryDao(BaseDao):
    def create(self, user_id: int, name: str, color: str) -> Category:
        id = self.exec('INSERT INTO category(user_id, name, color) VALUES (%s, %s, %s)', (user_id, name, color)).lastrowid
        return self.get(user_id, id)
    
    def exists(self, id: int) -> bool:
        return self.row_exist('category', 'id = %s', (id,))
    
    def get(self, user_id: int, id: int) -> Category:
        return Category.model_validate(
            self.exec('SELECT * FROM category WHERE user_id = %s AND id = %s', (user_id, id)).fetchone()
        )

    def get_all(self, user_id: int) -> List[Category]:
        return [Category.model_validate(category) for category in self.exec('SELECT * FROM category WHERE user_id = %s', (user_id,)).fetchall()]
    
    def update(self, user_id: int, id: int, category: CategoryUpdate):
        category_dict = category.model_dump(exclude_none=True)
        sql = generate_update_sql('category', category_dict, 'user_id = %s AND id = %s')
        self.exec(sql, [*category_dict.values(), user_id, id])

    def delete(self, user_id: int, id: int):
        self.exec('DELETE FROM category WHERE user_id = %s AND id = %s', (user_id, id)).rowcount