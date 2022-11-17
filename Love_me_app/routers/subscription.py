from fastapi import APIRouter
from schemas import Subscription
from typing import List
import models
from database import SessionLocal



router = APIRouter()

#<-- @madvirus work -->

db = SessionLocal()
@router.post("/api/subscription",response_model=Subscription,description="endpoint to post subscription")
async def subscribe(subscription:Subscription):
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


@router.get('/api/subscription/plans',description="list of available plans",response_model=List[Subscription])
async def SubscriptionPlans():
    plans = db.query(models.Subscription).all()
    return plans


#<-- @madvirus -->