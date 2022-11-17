from pydantic import BaseModel
from datetime import date,time,datetime

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

class Receiver(BaseModel):
    name:str
    email:str
    phone_number:str
    user_id:int
    date_created:datetime

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
    id:int
    name:str
    description:str
    months:int
    total_sms:int
    amount:int
    date_created:datetime

    # class config:
    #     orm_mode = True

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
