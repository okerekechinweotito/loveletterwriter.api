from fastapi import Depends,  HTTPException, Cookie, Header
from database import get_db
from sqlalchemy.orm import Session
from crud import UserCrud
from typing import Optional
from fastapi_jwt_auth import AuthJWT



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
