#Import libraries
from fastapi import APIRouter, HTTPException, status

#Import modules
import schemas, models
from database import get_db
from utils import get_password_hash, generate_access_token
from send_email import password_reset

#Initialize router and db
db = get_db()
router = APIRouter()

#create dummy variables and functions for endpoints
#pending when teammates will complete their tasks
website_url = "www.mechanic-team-engine.com"


#Endpoints
# TODO: Reset password routes

@router.post("/user/reset_request/", response_description="Password reset request")
async def reset_request(user_email: schemas.User):
    user = await db["users"].find_one({"email": user_email.email})

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
        return {"msg": "Email has been sent to the provided mail with instructions to reset your password."}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your details not found, invalid email address"
        )


@router.patch("user/reset_password/", response_description="Password reset")
async def reset_password(password_reset: schemas.ResetPass):
    reset_pass_data = {k:v for k, v in password_reset.dict().items() if v is not None}

    reset_pass_data["new_password"] = get_password_hash()
    return ("Successful")

