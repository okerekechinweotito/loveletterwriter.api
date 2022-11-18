from dependencies import get_current_user
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas

router=APIRouter()


@router.get("/user/me", dependencies=[Depends(get_current_user())])
def user_me(user: schemas.User):
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return {
        "firstname": user.firstname,
        "lastname": user.lastname,
        "email": user.email,
        "is_active": user.is_sub_active,
        "is_reminder": user.is_reminder,
        "date_joined": user.date_joined,
    }

@router.patch("/user/me", dependencies=[Depends(get_current_user())])
def update_profile(user:dict= Depends(get_current_user), db:Session = Depends(get_db)):

    user.update(user.dict(exclude_unset=True))
    db.commit()
    return {"User successfully updated"}
        

