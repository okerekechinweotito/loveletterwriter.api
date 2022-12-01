from fastapi import APIRouter,Depends,Request
from ..import  schemas 
from ..dependencies import get_current_user
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..import models
from ..database import get_db
from dotenv import load_dotenv
import os 
load_dotenv()
import stripe 

success_url = os.getenv("SUCCESS_URL")
cancel_url = os.getenv("CANCEL_URL")

router = APIRouter(tags=['subscription'])


@router.post("/api/v1/subscription",description="endpoint to post subscription")
async def subscribe(subscription:schemas.Subscription,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="please login")
    data = models.Subscription(
        name=subscription.name,
        description=subscription.description,
        months=subscription.months,
        amount=subscription.amount,
        date_created=subscription.date_created,
        plan_id = subscription.plan_id
    )
    db.add(data)
    try:

        db.commit()
        db.refresh(data)
    except Exception as e:
        print(str(e))


    return data 




@router.get('/api/v1/subscription/plans',description="list of available plans")
async def SubscriptionPlans(db: Session = Depends(get_db)):
    plans = db.query(models.Subscription).all()
    return plans



@router.post("/api/v1/subscription/checkout/{plan_id}")
async def subscribe_plan(plan_id:str,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):

    users = db.query(models.Customer).filter(models.Customer.user_id == user.id).first()
    CUSTOMER_ID = users.customer_id
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    querr = db.query(models.Subscription).filter(plan_id==plan_id).first()
    plans = querr
    if not user:
        raise HTTPException(status_code=401, detail="please signin")
    else:   
        try:

            sessions = stripe.checkout.Session.create(
                success_url = success_url,
                cancel_url = cancel_url,
                customer=CUSTOMER_ID,
                mode='subscription',
                subscription_data = {
                    'trial_period_days':1},
                payment_method_collection= "always",
                metadata = {
                    'user_id':user.id,
                    'user_name':user.first_name,
                    'user_email':user.email,
                    'plan_type':plans.name,
                    'month':plans.months
                },
                payment_method_types =["card"],
                    line_items =[{
                        'price':plan_id,
                        'quantity':1,
                    }
                    ]
                )
            return {"url":sessions['url']}
        except Exception as e:
            print(e)

        # return {"url":sessions['url']}




@router.patch("/api/v1/subscription/{plan_id}",description="edit plans")
async def UpdateSubscription(plan_id:int,request: schemas.SubscriptionBase,db:Session = Depends(get_db)):
    plans = db.query(models.Subscription).filter(models.Subscription.id == plan_id)
    plans.update(request.dict(exclude_unset=True))
    db.commit()
    return {"User successfully updated"}




