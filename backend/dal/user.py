from fastapi import Depends
from typing import Annotated

from model.user import UserLogin

class UserDao:
    def __init__(self, db):
        self._db = db
    
    def login(self, user: UserLogin):
        pass
    
    def create(self, user: UserLogin):
        pass
    
    def get(self, user: UserLogin):
        pass