"""
    amalthea - the world's history in the ethereum network

    GNU GENERAL PUBLIC LICENSE
"""
import sys
from fastapi import FastAPI
import fastapi_users

sys.path.insert(1, '../')
from persephone.auth import Auth


app = FastAPI()


app.include_router(
    Auth.fastapi_users.get_auth_router(Auth.jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"]
)

app.include_router(
    Auth.fastapi_users.get_register_router(Auth.on_after_register),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    Auth.fastapi_users.get_reset_password_router(
        Auth.SECRET,
        after_forgot_password=Auth.on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    Auth.fastapi_users.get_verify_router(
        Auth.SECRET,
        after_verification_request=Auth.after_verification_request
    ),
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    Auth.fastapi_users.get_users_router(),
    prefix="/users",
    tags=["user"]
)
