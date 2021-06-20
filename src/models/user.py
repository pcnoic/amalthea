"""
    Defining Amalthea User models.
"""
from fastapi_users import models
from fastapi_users.db import MongoDBUserDatabase
from pydantic.main import BaseModel


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass
