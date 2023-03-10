from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,date,time

from typing import Union
class User(BaseModel):
    first_name:str
    last_name:str
    password:str
    image:str
    email:EmailStr
    recovery_email:Union[EmailStr, None]
    facebook_id:Union[str, None]
    google_id:str
    twitter_id:Union[str, None]
    is_sub_active:bool
    sub_end_date:datetime
    is_reminder:bool
    date_created:datetime


class DisplayReceiver(BaseModel):
    id:int
    name:str
    email:EmailStr
    date_created:datetime
    class Config:
        orm_mode=True
class Receiver(BaseModel):
    email:EmailStr


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
    plan_id:str

    class config:
        orm_mode = True

class Transaction(BaseModel):
    user_id:int
    subscription_id:int
    ref_no:str
    date_created:str

    class config:
        orm_mode = True
        
class SubscriptionBase(BaseModel):
    name:str
    description:str
    months:str
    amount:float
    plan_id:str


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
    recovery_email:Union[EmailStr, None]
    twitter_id:Union[str, None]
    facebook_id:Union[str, None]

class UserCreate(UserBase):
    password:str=Field(min_length=6, description='password minimum length is 8 characters')

class Login(BaseModel):
    email:EmailStr
    password:str
class UserDetails(UserBase):
    id: int
    first_name:str
    last_name:str
    recovery_email: Union[EmailStr, None]
    twitter_id: Union[str, None]
    facebook_id: Union[str, None]
    is_sub_active:bool
    sub_end_date:Union[datetime, None]
    plan_type:Union[str, None]
    free_trial:bool
    is_reminder:bool
    date_created:datetime
    last_active:datetime

    class Config:
        orm_mode=True

class ImageUpdate(BaseModel):
    image:str

        
    class Config:
        orm_mode=True
from dotenv import load_dotenv
import os 
load_dotenv()
from fastapi_jwt_auth import AuthJWT
SECRET_KEY=os.getenv('SECRET_KEY', 'secret')

class Settings(BaseModel):
    authjwt_secret_key: str = os.getenv("SECRET_KEY")
    authjwt_token_location:set ={'cookies','headers'}
    authjwt_access_cookie_key:str='access_token'
    authjwt_refresh_cookie_key:str='refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite:str ='lax'


class Letter(BaseModel):
    id:int
    receiver_id:int
    letter:str
    title:str
    date_created:datetime

    class Config:
        orm_mode=True
 
class LoginDetails(BaseModel):
    access_token:str
    refresh_token:str
    user:UserDetails
    
    class Config:
        orm_mode=True

class Schedule_Letter(BaseModel):
    id:int
    schedule_time:datetime
    date_created:datetime
    letter:Letter



    class Config:
        orm_mode=True

class ContactUs(BaseModel):
    name:str
    email:EmailStr
    messages:str

class SendLetter(BaseModel):
    letter:str


@AuthJWT.load_config
def get_config():
    return Settings()

class ProductReviews(BaseModel):
    review:str
   
    
    # user: List[ProductReview]
   
    class Config:
        orm_mode = True


class PydanticReview(BaseModel):
    review:str
    id: int
    # first_name: str
    
    class Config:
        orm_mode = True

class RoleApplication(BaseModel):
    full_name: str
    email: str
    linked_in: str
    cover_letter: bytes
    cv: bytes

class PassReset(BaseModel):
    email:EmailStr 

class ValidateResetToken(BaseModel):
    token:str

class NewPassword(BaseModel):
    token:str
    password:str
class TranslateLetter(BaseModel):
    language:str
    letter:str
 
class MailSubscriber(BaseModel):
    email: EmailStr = Field(...)
    
    class Config:
        orm_mode = True

class GenerateLetter(BaseModel):
    partner_name: str
    occasion: str
    relationship: str
    inscription: str
    custom_words: Union[str, None] = None

class RoleName(str, Enum):
    admin = "admin"
    editor = "editor"
    contributor = "contributor"

class Admin(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    role: RoleName

    class Config:
        orm_mode=True
    
class AdminCreate(Admin):
    password:str
    
class AdminDetails(Admin):
    id: int
    approved: bool

class AdminLoginDetails(BaseModel):
    access_token:str
    refresh_token:str
    user:Admin
    
    class Config:
        orm_mode=True



class Statistics(BaseModel):
    mail_subscribers: int
    users: int
    letters: int
    admins:int
class Feedback(BaseModel):
    is_helpfull: bool
    feedback: str

class ChatBot(BaseModel):
    question: str
