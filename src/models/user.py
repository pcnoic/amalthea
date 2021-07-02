"""
    Defining Amalthea User models.
"""
from fastapi_users import models
from pydantic import BaseModel

class User(models.BaseUser):
    username: str


class UserCreate(models.BaseUserCreate):
    username: str


class UserUpdate(models.BaseUserUpdate):
    username: str


class UserDB(User, models.BaseUserDB):
    username: str
    
class WikiUser(BaseModel):
    password: str
