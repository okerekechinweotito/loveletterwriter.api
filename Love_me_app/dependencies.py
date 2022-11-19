from fastapi import Depends,  HTTPException, Cookie, Header
from .database import get_db
from sqlalchemy.orm import Session
from .crud import UserCrud
from typing import Optional
from fastapi_jwt_auth import AuthJWT
from . import models
from google.oauth2 import id_token
from google.auth.transport import requests
from .utils import hash_password
from dotenv import load_dotenv
import os 
load_dotenv()



def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    try:

        Authorize.jwt_required()
        user_id=Authorize.get_jwt_subject()
        user=UserCrud.get_user_by_id(db, user_id)
        return user
    except:
        raise exception


def get_user_sub_is_active(user:dict=Depends(get_current_user)):
    if not user.is_sub_active:
        raise HTTPException(status_code=401, detail='your subscription has expired')
    return True

def google_auth(token:str, db:Session=Depends(get_db)):
    try:
        token= id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        user=UserCrud.get_user_by_email(db, email=token['email'])
        if user:
            return user
        else:
            user=models.User(email=token['email'], first_name=token['family_name'], last_name=token['given_name'], google_id=token['sub'], password=hash_password(token['sub']))
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
    except:
        raise HTTPException(status_code=400, detail='invalid token or token has expired')
