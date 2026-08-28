from schemas.user import UserBase, UserId
from database.models.base import BaseDBModel

class User(UserBase, BaseDBModel):
    id: UserId
    hash_password: str