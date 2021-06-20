"""
    Defining Amalthea User models.
"""
from config import ConfigParams
from fastapi import FastAPI
from fastapi_users import models
from fastapi_users.db import MongoDBUserDatabase


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass
