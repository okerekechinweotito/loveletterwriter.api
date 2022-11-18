from fastapi import APIRouter
from fastapi import  Depends,  HTTPException, APIRouter,Cookie, Header
import crud, schemas
from fastapi.responses import Response
from database import get_db
from fastapi_jwt_auth import AuthJWT
from utils import  authenticate, REFRESH_TOKEN_LIFETIME, ACCESS_TOKEN_LIFETIME_MINUTES, access_cookies_time, refresh_cookies_time
from sqlalchemy.orm import Session
user_crud=crud.UserCrud
from datetime import timedelta

router=APIRouter()



@router.post('/signup/', response_model=schemas.UserDetails, summary='endpoint for users to signup', status_code=201, tags=['auth'])
def signup(user:schemas.UserCreate, db:Session=Depends(get_db)):
    '''
    endpoint to signup users 
    '''

    if  user_crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='user with this email already exists')
    return user_crud.create_user(db, user)


@router.post('/login', status_code=200, tags=['auth'], summary='endpoint to login users')
def Login( response:Response,login:schemas.Login,Authorize:AuthJWT=Depends() ,db:Session=Depends(get_db)):
    '''
    if authentication is sucessful access_token and refresh_token will be given which should be passed in the header or sent with the cookie to access protected resource.
    its preferable if tokens are sent with cookies because it is httponly which prevents clients from accessing it.
    * access token lifetime is 5minutes
    * rfresh token lifetime is 14 days
    '''
    password, email=login.password, login.email
    user=authenticate(db=db, password=password, email=email)
    access_token=Authorize.create_access_token(subject=user.id, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=Authorize.create_refresh_token(subject=user.id, expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token}


@router.post('/refresh-token', tags=['auth'], summary='enpoint to get new access token')
def refresh_token(response:Response,Authorization:AuthJWT=Depends(), refresh_token:str=Cookie(default=None), Bearer:str=Header(default=None)):
    '''
    To get new access token the refresh token giving during signup must be passed in the header or sent with the cookie.
    its preferable to pass to make use of the cookie because it's httponly which prevents clients from accessing it.
    '''
    exception=HTTPException(status_code=401, detail='invalid refresh token or token has expired')
    try:
        Authorization.jwt_refresh_token_required()
        current_user=Authorization.get_jwt_subject()
        access_token=Authorization.create_access_token(current_user)
        response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
        return {'access_token':access_token}
    except:
        raise exception




@router.post('/logout',tags=['auth'],summary='endpoint to logout users')
def logout(Authorize:AuthJWT=Depends()):
    '''
    if requests where made through headers the token should be deleted from the client side.
    if made with cookies they will be deleted here.
    '''
    Authorize.unset_jwt_cookies()
    return {'message':'successfully logout'}