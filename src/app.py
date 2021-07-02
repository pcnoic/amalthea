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

# Application controllers
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

###### Endpoints
# Identity
@app.get("/")
def root(user: User = Depends(Auth.fastapi_users.current_user())):
    return {"message":"Amalthea API - welcome {username}".format(
        username = user.id
    )}
 
@app.post("/get-wiki-id", status_code=200)
async def get_wiki_id(wikiuser: WikiUser, response: Response, user: User = Depends(Auth.fastapi_users.current_user())):
    wiki_id = get_wikiId(user.username, wikiuser.password)
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
async def verify(response: Response, am_wikiID: Optional[str] = FC(None), user: User = Depends(Auth.fastapi_users.current_user())):
    verifiable = cookie_manager.sign(user.username)
    print(verifiable)
    if bool(am_wikiID):
        cookie_split = am_wikiID.split(";")
        print(cookie_split[1])
        if verifiable == cookie_split[1]:
            response.delete_cookie(
                key="am_wikiID"
            )
            return {"message":"successful"}
        else:
            response.delete_cookie(
                key="am_wikiID"
            )
            return {"message":"failed"}
    else:
        return {"message":"cookie is missing"}


# WikiPedia Revisions
@app.get("/articles/{keyword}/get", status_code=200)
def get_articles(keyword: str, response: Response, user: User = Depends(Auth.fastapi_users.current_user())):
    return Revisions.search_wiki(keyword)

@app.get("/articles/revisions/{pageid}/get", status_code=200)
def get_article_revisions(pageid: str, response: Response, user: User = Depends(Auth.fastapi_users.current_user())):
    return Revisions.get_own_revisions(user.username, pageid)

@app.get("/articles/revisions/content/{revid}/get", status_code=200)
def get_revision_content(revid: str, response: Response, user: User = Depends(Auth.fastapi_users.current_user())):
    return Revisions.get_revision_content(revid)
