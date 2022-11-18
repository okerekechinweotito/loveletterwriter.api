from dependencies import get_current_user
from fastapi import Depends, APIRouter
from fastapi import APIRouter
router=APIRouter()
@router.get("/user/me")
def user_me(user:dict=Depends(get_currrent_user)):
    #   return {'user':user}
    return {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "is_active": user.is_sub_active,
        "is_reminder": user.is_reminder,
        "date_joined": user.date_joined,
    }

@router.patch("/user/me")
def update_profile(user:dict= Depends(get_current_user)):

    user.update(user.dict(exclude_unset=True))
    return {
        "firstname": ,
        "lastname": ,
        "is_active": ,
    }