from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from Love_me_app.models import User,Letter
from Love_me_app.database import get_db
from Love_me_app.dependencies import get_current_user
from Love_me_app.schemas import AdminCreate, UserCreate,UserDetails,UserUpdate
from Love_me_app.utils import hash_password

router = APIRouter(tags=['Admin'],prefix="/api/v1/admin")


def get_subscribers( db:Session = Depends(get_db),skip: int=0, limit:int = 15):
    return db.query(User).offset(skip).limit(limit).all()

def get_number_of_letters(db:Session = Depends(get_db)):
    letters = db.query(Letter).all()
    return len(letters)

def get_number_subscribers(db:Session = Depends(get_db)):
    subscribers = db.query(User).all()
    return len(subscribers)


@router.post('/user', response_model=UserDetails)
def add_admin(admin: AdminCreate, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    current_user = user
    if current_user is not None:
    # if current_user is not None and current_user.is_admin:
        password=hash_password(admin.password)
        new_admin=User(email=admin.email, password=password, first_name=admin.first_name, last_name=admin.last_name, is_admin=True,role=admin.role)
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
        return new_admin
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")

@router.get("/statistics")
def add_admin(user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    current_user = user
    if current_user is not None and current_user.is_admin:

        statistics = {
            'number_subscribers': get_number_subscribers(),
            'number_letters': get_number_of_letters(),
        }

        return statistics

    


