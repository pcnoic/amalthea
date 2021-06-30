"""
    amalthea - the world's history

    GNU GENERAL PUBLIC LICENSE
"""
import sys
from typing import Optional
from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi import Cookie as FC
import fastapi


# Relative modules
sys.path.insert(1, '../')
from persephone.auth import Auth
from persephone.wikimedia_auth import get_wikiId
from hermes.revisions import Revisions
from models.user import User, WikiUser
from persephone.crypto import Cookie


app = FastAPI()
router = APIRouter()
cookie_manager = Cookie()

# Routers
app.include_router(
    Auth.fastapi_users.get_auth_router(Auth.jwt_authentication),
    prefix="/auth/jwt",
    tags=["auth"]
)

# Refresh token
@router.post("/auth/jwt/refresh")
async def refresh_jwt(response: Response, user=Depends(Auth.fastapi_users.get_current_active_user)):
    return await Auth.jwt_authentication.get_login_response(user, response)

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
    Auth.fastapi_users.get_users_router(),
    prefix="/users",
    tags=["user"]
)

# Endpoints
@app.get("/")
def root(user: User = Depends(Auth.fastapi_users.current_user())):
    return {"message":"Amalthea API - welcome {username}".format(
        username = user.id
    )}

@app.post("/get-wiki-id", status_code=200)
async def get_wiki_id(user: WikiUser, response: Response):
    wiki_id = get_wikiId(user.username, user.password)
    cookie_hmac_signature = cookie_manager.sign(wiki_id)
    cookie_value = wiki_id + ";" + cookie_hmac_signature 
    response.set_cookie(
        key="am_wikiID", 
        value=cookie_value,
        httponly=True,
        expires=60,
        samesite="Strict"    
    )
    return {"message":"Come to the dark side, we have cookies."}
    
@app.post("/verify", status_code=200)
async def verify(am_wikiID: Optional[str] = FC(None), user: User = Depends(Auth.fastapi_users.current_user())):
    verifiable = cookie_manager.sign(user.username)
    print(verifiable)
    if bool(am_wikiID):
        cookie_split = am_wikiID.split(";")
        print(cookie_split[1])
        if verifiable == cookie_split[1]:
            return {"message":"successful"}
        else:
            return {"message":"failed"}
    else:
        return {"message":"cookie is missing"}
# 
# @app.get("/revisions/{article_id}/get", status_code=200)
# def get_article_revisions(article_id: str, response: Response):
    # return Revisions.get_own_revisions(article_id)
# 
