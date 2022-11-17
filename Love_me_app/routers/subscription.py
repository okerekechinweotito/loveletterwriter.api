from fastapi import APIRouter
from models import * 
from schemas import *
from database import engine,SessionLocal



router = APIRouter()

db = SessionLocal()
@router.post("/sub",response_model=Subscription)
async def subsc(subscription:Subscription):
    data = Subscription(
        id = subscription.id,
        name=subscription.name,
        description=subscription.description,
        months=subscription.months,
        total_sms=subscription.total_sms,
        amount=subscription.amount,
        date_created=subscription.date_created
    )
    db.add(data)
    db.commit()


    return data 
