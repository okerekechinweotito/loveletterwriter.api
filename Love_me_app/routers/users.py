from dependencies import get_current_user
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session 

router=APIRouter(tags=['User'],prefix="/api/v1/user/me")


@router.get("/", dependencies=[Depends(get_current_user())])
def user_me(user: schemas.User):
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    return {
        "firstname": user.first_name,
        "lastname": user.last_name,
        "email": user.email,
        "is_active": user.is_sub_active,
        "is_reminder": user.is_reminder,
        "date_joined": user.date_created,
    }

@router.patch("/", dependencies=[Depends(get_current_user())])
def update_profile(user: schemas.User, db:Session = Depends(get_db)):
    user.update(user.dict(exclude_unset=True))
    db.commit()
    return {"User successfully updated"}
        

