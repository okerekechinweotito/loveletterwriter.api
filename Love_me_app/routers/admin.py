from fastapi import APIRouter,Depends,HTTPException,status,Header,Cookie
from sqlalchemy.orm import Session
from Love_me_app.models import User,Letter,Admin, MailSubscriber
from Love_me_app.database import get_db
from Love_me_app.schemas import AdminCreate, AdminDetails, AdminLoginDetails, Login, Statistics,UserDetails
from Love_me_app.utils import hash_password, verify_password
from fastapi_jwt_auth import AuthJWT
from datetime import timedelta
from fastapi.responses import Response
from fastapi_pagination import Page,add_pagination,paginate

from dotenv import load_dotenv
import os
load_dotenv()

router = APIRouter(prefix="/api/v1/admin")


ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24


def get_admin_mail(db:Session, email):
    return db.query(Admin).filter(Admin.email==email).first()

def get_admin_by_id(db:Session, id):
    return db.query(Admin).filter(Admin.id==id).first()

def authenticate(db:Session,email:str, password:str):
    user = db.query(Admin).filter(Admin.email == email).first()
    print(user.approved)
    if not user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='invalid email or password')
    if not verify_password(password, user.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='invalid email or password')
    if not user.approved:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='You need to be approved to get access')
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        "id": user.id,
        "approved": user.approved,
        "email": user.email,
        "role": user.role
    }



def get_current_user(authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    try:
        authorize.jwt_required()
        user_id=authorize.get_jwt_subject()
        user=get_admin_by_id(db, user_id)
        return user
    except:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

def logout(authorize:AuthJWT):
    authorize.unset_jwt_cookies()
    return {
        "Logged Out",
    }

def get_subscribers( db:Session = Depends(get_db)):
    return db.query(User).all()

def get_mail_subscribers( db:Session = Depends(get_db),skip: int=0, limit:int = 15):
    return db.query(MailSubscriber).offset(skip).limit(limit).all()

def get_all_admins(db,skip:int, limit:int):
    return db.query(Admin).offset(skip).limit(limit).all()

def get_mail_subscribers(db:Session):
    mail_subscribers = db.query(MailSubscriber).all()
    return len(mail_subscribers)

def get_number_of_letters(db:Session):
    letters = db.query(Letter).all()
    return len(letters)

def get_number_subscribers(db:Session):
    subscribers = db.query(User).all()
    return len(subscribers)

def get_number_admins(db:Session):
    admins = db.query(Admin).all()
    return len(admins)

def get_user_by_id(db:Session,id):
    return db.query(User).filter(User.id==id).first()

def get_mail_subscriber(db:Session, id):
    return db.query(MailSubscriber).filter(MailSubscriber.id==id).first()

def create_admin(db:Session,admin:AdminCreate):
    password=hash_password(admin.password)
    if get_admin_mail(db,email=admin.email):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Email already in use')
    else:
        new_admin=Admin(email=admin.email, password=password, first_name=admin.first_name, last_name=admin.last_name,role=admin.role)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
  

    
@router.post('/signup',tags=['Admin Auth'], response_model=AdminDetails)
def create_admin_(admin_:AdminCreate,db:Session=Depends(get_db)):
    #current_user = user
    #if current_user is not None:
        admin = Admin(**admin_.dict())
        new_admin = create_admin(db=db,admin=admin)
        return new_admin
    #raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired')

@router.post('/login',response_model=AdminLoginDetails,tags=["Admin Auth"])
def log_admin(login:Login,response:Response, db:Session=Depends(get_db),authorize:AuthJWT=Depends()):
    user=authenticate(db=db, password=login.password, email=login.email)
    access_token=authorize.create_access_token(subject=user['id'], expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=authorize.create_refresh_token(subject=user['id'], expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}



@router.post('/refresh-token',tags=["Admin Auth"])
def refresh_token(response:Response,authorization:AuthJWT=Depends(), refresh_token:str=Cookie(default=None), Bearer:str=Header(default=None)):
    
    try:
        authorization.jwt_refresh_token_required()
        current_user=authorization.get_jwt_subject()
        access_token=authorization.create_access_token(current_user)
        response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
        return {'access_token':access_token}
    except:
        raise HTTPException(status_code=401, detail='invalid refresh token or token has expired')


@router.post('/logout',tags=["Admin Auth"])
def log_out(authorize_: AuthJWT=Depends()):
    logout(authorize=authorize_)

@router.patch('/{admin_id}/approve',tags=["Admin"], response_model=AdminDetails)
def approve(admin_id,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        admin = db.query(Admin).filter(Admin.id==admin_id).first()
        if admin is not None:
            if admin.approved:
                admin.approved = False
                db.commit()
                db.refresh(admin)
                return admin
            if not admin.approved:
                admin.approved = True
                db.commit()
                db.refresh(admin)
                return admin
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired')

@router.get('/statistics',tags=['Admin'] ,response_model=Statistics)
def return_statistics(user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        stats = {
        'mail_subscribers': get_mail_subscribers(db=db),
        'users': get_number_subscribers(db=db),
        'letters': get_number_of_letters(db=db),
        'admins': get_number_admins(db=db)
        }

        return stats
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})
    

@router.get('/admins/all',tags=['Admin'] ,response_model=Page[AdminDetails])
def return_admin_list(user:dict=Depends(get_current_user),db:Session= Depends(get_db),skip: int=0, limit:int = 15):
    current_user = user
    if current_user is not None:
        admins = get_all_admins(db=db, skip=skip, limit=limit)
        return paginate(admins)
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.get('/subscribers/all',tags=['Admin'] ,response_model=Page[UserDetails])
def return_subscriber_list(user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        users = get_subscribers(db=db)
        return paginate(users)
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.delete('/{admin_id}',tags=['Admin'])
def delete_single_admin(admin_id,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        ad = db.query(Admin).filter(Admin.id==admin_id).first()
        if ad:
            db.delete(ad)
            return {"Deleted Successfully"}
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="Entry not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.delete('/user/{user_id}',tags=['Admin'])
def delete_single_user(user_id,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        user = db.query(User).filter(User.id==user_id).first()
        if user is not None:
            if user.is_sub_active:
                 return{
                    "This User has an active Subscription"
                 }
            else:
                db.delete(user)
                db.commit()
                return {
                "Deleted Successfully"
                }
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.delete('/user/mail/{user_id}',tags=['Admin'])
def delete_single_mail_subscriber(user_id,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        user = db.query(MailSubscriber).filter(MailSubscriber.id== user_id).first()
        if user is not None:
            db.delete(user)
            db.commit()
            return {
                "Deleted"
            }
        
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

@router.post('/admin/del',tags=['Admin'])
def delete_multi_admins(admins:list,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
            entries = db.query(Admin).filter(Admin.id.in_(admins)).all()
            for entry in entries:
                db.delete(entry)
                db.commit()
            return {
                'entries': len(entries),
                'message': 'deleted'
            }     
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='Access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.post('/multiple/users/mail/',tags=['Admin'])
def delete_multiple_mail_subscribers(multiple_ids:list,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        entries = db.query(MailSubscriber).filter(MailSubscriber.id.in_(multiple_ids)).all()
        for entry in entries:
            db.delete(entry)
            db.commit()
            return {
                'entries': len(entries),
                'message': 'deleted'
            }     
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})


@router.post('/multiple/users/',tags=['Admin'])
def delete_multiple_users(multiple_ids:list,user:dict=Depends(get_current_user),db:Session= Depends(get_db)):
    current_user = user
    if current_user is not None:
        entries = db.query(User).filter(User.id.in_(multiple_ids)).all()
        for entry in entries:
            db.delete(entry)
            db.commit()
            return {
                'entries': len(entries),
                'message': 'deleted'
            }
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})



@router.get('/initial',tags=['Intial'])
def execute_initial_admin(db:Session= Depends(get_db)):
    password_ = os.getenv("SUPER_ADMIN_PASSWORD")
    new_admin = Admin(
    first_name = "junior",
    last_name = "admin",
    email = os.getenv("SUPER_ADMIN_EMAIL"),
    password = hash_password(password_),
    role = "admin",
    approved = True,
    )
    user = get_admin_mail(db=db, email=new_admin.email)
    if user is None:
        try:
            db.add(new_admin)
            db.commit()
            db.refresh(new_admin)
            return {"initial created"}
        except Exception as e:
            print(e)
    else:
        return {"Already exists"}
        







    






add_pagination(router)