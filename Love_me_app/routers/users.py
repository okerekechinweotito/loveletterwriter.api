"""
User endpoints for requesting password reset link and resetting password
"""

#Import libraries
from fastapi import APIRouter, HTTPException, status, Depends, Cookie, Header
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT

#Import modules
from ..send_email import password_reset_email
from ..utils import  hash_password, ACCESS_TOKEN_LIFETIME_MINUTES
from ..crud import UserCrud
from .. import schemas
from ..database import get_db

#Initialize router and db
db = get_db()
router = APIRouter(tags=['reset password'],prefix="/api/v1/user")

#Function to get current user
def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    try:

        Authorize.jwt_required()
        user_id=Authorize.get_jwt_subject()
        user=UserCrud.get_user_by_id(db, user_id)
        return user
    except:
        raise exception


#Endpoints
# TODO: Reset password request route

@router.post("/reset_request/", response_description="Password reset request")
async def reset_request(requesting_user: schemas.PasswordResetRequest, Authorize:AuthJWT=Depends()):
    user = UserCrud.get_user_by_email(db, requesting_user.email)


    if user is not None:
        token=Authorize.create_access_token(subject=user.id, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))

        reset_link = f"loveme.zuri.team/user/password_reset?token={token}"


        await password_reset_email("Password Reset", user["email"],
            {
                "title": "Password Reset",
                "name": user["name"],
                "reset_link": reset_link
            }
        )
        return {"msg": "Password reset email sent successfully."}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your details not found, invalid email address"
        )

# TODO: Reset password route
@router.patch("/reset_password/", response_description="Password reset")
async def reset_password(token: str, password_reset: schemas.PasswordReset):
    reset_pass_data = {k:v for k, v in password_reset.dict().items() if v is not None}


    reset_pass_data["password"] = hash_password(reset_pass_data["new_password"])
    
    if len(reset_pass_data) >= 1:
        # Get current user from session token
        user = await get_current_user(token)

        # Modify password of the current user
        update_result = await db["users"].update_one({"id": user["id"]}, {"$set": reset_pass_data})

        if update_result.modified_count == 1:
            # get the newly updated current user and return as a response
            updated_user = await db["users"].find_one({"id": user["id"]})
            if(updated_user) is not None:
                return updated_user

    existing_user = await db["users"].find_one({"id": user["id"]})
    if(existing_user) is not None:
        return existing_user

    # Raise error if a user with that email and id can not be found in the database
    raise HTTPException(status_code=404, detail=f"User not found")

