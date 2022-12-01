from fastapi import APIRouter,Depends,HTTPException,status,Header,Cookie
from sqlalchemy.orm import Session
from Love_me_app.models import User,Letter,Admin, MailSubscriber
from Love_me_app.database import get_db
from Love_me_app.schemas import AdminCreate, AdminDetails, UserCreate,UserDetails,UserUpdate
from Love_me_app.utils import hash_password, verify_password
from fastapi_jwt_auth import AuthJWT


router = APIRouter(tags=['Admin'],prefix="/api/v1/admin")



def get_admin_mail(db:Session, email):
    return db.query(Admin).filter(Admin.email==email).first()

def get_admin_by_id(db:Session, id):
    return db.query(Admin).filter(Admin.id==id).first()
def authenticate(db:Session,email:str, password:str):
    user = db.query(Admin).filter(Admin.email == email).first()
    if not user:
        raise HTTPException(status_code=400, detail='invalid email or password')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='invalid email or password')
    return user


def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})
    try:
        Authorize.jwt_required()
        user_id=Authorize.get_jwt_subject()
        user=get_admin_by_id(db, user_id)
        return user
    except:
        raise exception


def get_subscribers( db:Session = Depends(get_db),skip: int=0, limit:int = 15):
    return db.query(User).offset(skip).limit(limit).all()


def get_mail_subscribers( db:Session = Depends(get_db),skip: int=0, limit:int = 15):
    return db.query(MailSubscriber).offset(skip).limit(limit).all()

def get_mail_subscribers(db:Session):
    mail_subscribers = db.query(MailSubscriber).all()
    return len(mail_subscribers)

def get_number_of_letters(db:Session):
    letters = db.query(Letter).all()
    return len(letters)

def get_number_subscribers(db:Session):
    subscribers = db.query(User).all()
    return len(subscribers)



def create_admin(db:Session,admin:AdminCreate):
    password=hash_password(admin.password)
    if get_admin_mail(db,email=admin.email):
        raise HTTPException(status_code=400, detail='Email already in use')
    else:
        new_admin=Admin(email=admin.email, password=password, first_name=admin.first_name, last_name=admin.last_name,role=admin.role)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    

def delete_single_entry(db:Session, id):
    if get_admin_by_id(db,id=id):
        db.delete(get_admin_by_id(db,id))
        db.commit()
        return {"Entry deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already in use")


def delete_multiple_entries(db:Session, entries:list):
    for id in entries:
        try:
            entry = get_admin_by_id(db,id)
            db.delete(entry)
            db.commit()
            return {"Entries deleted"}
        except Exception as e:
            return {"Error": e.message}
        

        



    




