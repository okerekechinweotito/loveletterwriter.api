"""
User endpoints for resetting password
Modules needed for these endpoints that are being worked on by others
have been 'simulated' in the dependencies.py file and have been imported
This is to ensure that once the branches are merged, everything should 
work as expected
"""

#Import libraries
from fastapi import APIRouter, HTTPException, status, Depends
from send_email import password_reset
from dependencies import get_current_user, website_url
from utils import generate_access_token, get_password_hash
from crud import UserCrud
#Import modules
import schemas, models
from database import get_db

#Initialize router and db
db = get_db()
router = APIRouter()


#Endpoints
# TODO: Reset password request route

@router.post("/user/reset_request/", response_description="Password reset request")
async def reset_request(requesting_user: schemas.ResetPasswordRequest):
    user = UserCrud.get_user_by_id(db, requesting_user.user_id)


    if user is not None:
        token = generate_access_token({"id": user["id"]})

        reset_link = f"{website_url}user/password_reset?token={token}"


        await password_reset("Password Reset", user["email"],
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
@router.patch("user/reset_password/", response_description="Password reset")
async def reset_password(token: str, password_reset: schemas.ResetPassword):
    reset_pass_data = {k:v for k, v in password_reset.dict().items() if v is not None}


    reset_pass_data["password"] = get_password_hash(reset_pass_data["new_password"])
    
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

