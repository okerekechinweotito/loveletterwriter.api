from fastapi import APIRouter,Depends
import  schemas 
from sqlalchemy.orm import Session
import models
from database import get_db



router = APIRouter()

#<-- @madvirus work -->

@router.post("/api/subscription",description="endpoint to post subscription")
async def subscribe(subscription:schemas.Subscription,db: Session = Depends(get_db)):
    data = models.Subscription(
        name=subscription.name,
        description=subscription.description,
        months=subscription.months,
        total_sms=subscription.total_sms,
        amount=subscription.amount,
        date_created=subscription.date_created
    )
    db.add(data)
    db.commit()
    db.refresh(data)


    return data 


@router.get('/api/subscription/plans',description="list of available plans")
async def SubscriptionPlans(db: Session = Depends(get_db)):
    plans = db.query(models.Subscription).all()
    return plans





@router.post("/subscription/plans/{id}")
async def subscribe_plan(id:int,subscription:schemas.Subscription):
    pass



#<-- @madvirus -->