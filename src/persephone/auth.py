import motor.motor_asyncio
from fastapi import Request
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import MongoDBUserDatabase
from models.user import * 

class Auth:
    
    SECRET = "foo" # TODO: make this something actually secret
    auth_backends = []
    
    jwt_authentication = JWTAuthentication(
        secret=SECRET, lifetime_seconds=3600, tokenUrl="auth/jwt/login"
    ) 
    

    client = motor.motor_asyncio.AsyncIOMotorClient(
        ConfigParams.MONGODB_HOST, uuidRepresentation="standard"
    )
    db = client[ConfigParams.MONGODB_DBNAME]
    col = db["users"]

    user_db = MongoDBUserDatabase(UserDB, col)


    def on_after_register(user: UserDB, request: Request):
        print(f"User {user.id} has regisered.")



    def on_after_forgot_password(user: UserDB, request: Request):
        print(f"User {user.id} has registered.")



    def after_verification_request(user: UserDB, token: str, request: Request):
        print(f"Verification requested for {user.id}. Verification token: {token}")

    
    
    fastapi_users = FastAPIUsers(
        user_db,
        auth_backends,
        User,
        UserCreate,
        UserUpdate,
        UserDB,  
    )
