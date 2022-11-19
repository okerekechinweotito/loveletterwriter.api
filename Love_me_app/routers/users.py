from ..dependencies import get_current_user
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session 

router=APIRouter(tags=['User'],prefix="/api/v1/user/me")

"""
endpoint to get a user profile. The user has to be logged in already.

"""
@router.get("/")
def user_me(user:dict=Depends(get_current_user)):
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


"""
endpoint to update user profile by getting the current user email and updating their profile.
"""
@router.patch("/",)
def update_profile(request: schemas.UserBase, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    profile = db.query(models.User).filter(models.User.id)
    profile.update(request.dict(exclude_unset=True))
    db.commit()
    return {"User successfully updated"}
        
