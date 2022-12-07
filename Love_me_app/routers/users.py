"""
User endpoints for requesting password reset link and resetting password
"""

#Import libraries
from fastapi import APIRouter, HTTPException, status, Depends, Cookie, Header
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi_jwt_auth import AuthJWT
import string, random, shutil

#Import modules
from ..send_email import password_reset_email
from ..utils import  hash_password, ACCESS_TOKEN_LIFETIME_MINUTES
from ..crud import UserCrud
from .. import schemas, models
from ..database import get_db
from ..dependencies import get_current_user

# Image Upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image

#Initialize router and db
db = get_db()
router=APIRouter(tags=['User'],prefix="/api/v1/user/me")


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



"""
endpoint to get a user profile. The user has to be logged in already.

"""
@router.get("/get-user")
def user_me(user:dict=Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="user not found")
    return {
        "firstname": user.first_name,
        "lastname": user.last_name,
        "email": user.email,
        "image":user.image,
        "recovery_email": user.recovery_email,
        "facebook_id": user.facebook_id,
        "twitter_id": user.twitter_id,
        "is_active": user.is_sub_active,
        "is_reminder": user.is_reminder,
        "date_joined": user.date_created,
        "sub_end":user.sub_end_date,
        "plan_type":user.plan_type,
        
    }
"""
endpoint to update user profile by getting the current user email and updating their profile.
"""
@router.patch("/update-user")
def update_profile(request: schemas.UserBase, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    if user.email==request.email:
        profile = db.query(models.User).filter(models.User.id==user.id).first()
        profile.email=request.email
        profile.first_name=request.first_name
        profile.last_name=request.last_name
        profile.recovery_mail=request.recovery_email
        profile.twitter_id=request.twitter_id
        profile.facebook_id=request.facebook_id
        db.commit()
        db.refresh(profile)
        return {"User successfully updated"}

    elif UserCrud.get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="user with this email already exists")
 
    profile = db.query(models.User).filter(models.User.id==user.id).first()
    profile.email=request.email
    profile.first_name=request.first_name
    profile.last_name=request.last_name
    profile.recovery_mail=request.recovery_email
    profile.twitter_id=request.twitter_id
    profile.facebook_id=request.facebook_id
    db.commit()
    db.refresh(profile)
    return {"User successfully updated"}


"""
function to process user profile picture to string(url)
"""      
async def get_image_url(file: UploadFile = File(...)):
    FILEPATH = "./static/"
    filename = file.filename
    extension= filename.split(".")[1]
    if extension not in ['png', 'jpg']:
        return {'status': "error", 'detail':"Image type not allowed"}
    token_name= secrets.token_hex(8)+"."+extension
    generated_name=FILEPATH + token_name
    file_content= await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    #PILLOW IMAGE RESIZE
    img = Image.open(generated_name)
    resized_image = img.resize(size=(200, 200))
    resized_image.save(generated_name)
    
    file.close()
    file_url = generated_name[1:]
    return file_url
    

"""
endpoint to update user profile picture by getting the current user email and updating their profile.
"""    
@router.post('/upload-image',)   
async def upload_image(image: UploadFile = File(...), user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    if not user:
        raise  HTTPException(status_code=404, detail="User not found")
    current_user= db.query(models.User).filter(models.User.id == user.id)
    image_url = await get_image_url(image)
    current_user.update({models.User.image: image_url}, synchronize_session=False)
    db.commit()
    db.close()
    return {'profile_image': image_url, "details":"Check Your Profile.." }



"""
endpoint to update user profile image to app's default profile image
"""   
@router.patch("/remove-image")
async def remove_image(user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=404, detail="User not Found")
    current_user= db.query(models.User).filter(models.User.id == user.id)
    default_user_image ="/static/default_user_image.jpg"
    current_user.update({models.User.image : default_user_image}, synchronize_session=False)
    db.commit()
    db.close()
    return{"Profile Image Removed"}