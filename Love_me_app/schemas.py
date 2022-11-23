from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,date,time

from typing import Union
class User(BaseModel):
    first_name:str
    last_name:str
    password:str
    email:str
    facebook_id:str
    google_id:str
    is_sub_active:bool
    sub_end_date:datetime
    is_reminder:bool
    date_created:datetime

class DisplayReceiver(BaseModel):
    name:str
    email:str
    phone_number:str
    user_id:int
    date_created:datetime
    class Config:
        orm_mode=True
class Receiver(BaseModel):
    name:str
    email:str
    phone_number:str

class Letter(BaseModel):
    user_id:int
    receiver_id:int
    letter:str
    date_created:datetime

class Schedule(BaseModel):
    user_id:int
    receiver_id:int
    schedule_time:datetime
    date_created:datetime

class AiTrainer(BaseModel):
    ui_name:str
    ai_word:str
    date_created:datetime

class AiTrainerValue(BaseModel):
    ai_trainer_id:int
    user_id:int
    receiver_id:int
    value:str
    date_created:datetime

class Subscription(BaseModel):
    name:str
    description:str
    months:int
    amount:float
    date_created:datetime

    class config:
        orm_mode = True

class Transaction(BaseModel):
    user_id:int
    subscription_id:int
    ref_no:str
    date_created:str

    class config:
        orm_mode = True
        

class ResetPass(BaseModel):
    pin:str
    user_id:int
    is_used:bool
    expiry_date:datetime
    date_created:datetime

class BlackListedTokens(BaseModel):
    token:str
    expiry_date:datetime
    blacklisted_on:datetime

class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(...)

class PasswordReset(BaseModel):
    password: str = Field(...)
    confirm_password: str = Field(...)


class UserBase(BaseModel):
    first_name: str
    last_name:str
    email: EmailStr

class UserCreate(UserBase):
    password:str=Field(min_length=8, description='password minimum length is 8 characters')

class Login(BaseModel):
    email:EmailStr
    password:str
class UserDetails(UserBase):
    id: str
    first_name:str
    last_name:str
    is_sub_active:bool
    sub_end_date:Union[datetime, None]=None
    is_reminder:bool
    date_created:datetime

    class Config:
        orm_mode=True
from dotenv import load_dotenv
import os 
load_dotenv()
from fastapi_jwt_auth import AuthJWT
SECRET_KEY='random'

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_token_location:set ={'cookies','headers'}
    authjwt_access_cookie_key:str='access_token'
    authjwt_refresh_cookie_key:str='refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite:str ='lax'


@AuthJWT.load_config
def get_config():
    return Settings()

class ProductReviews(BaseModel):
    review:str
    

    class Config:
        orm_mode = True

