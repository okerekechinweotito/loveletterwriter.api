from fastapi import APIRouter,Depends,Request
from ..import  schemas 
from datetime import datetime
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
async def add_subscribtion_plans(subscription:schemas.Subscription,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):
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
async def get_subscription_plans(db: Session = Depends(get_db)):
    plans = db.query(models.Subscription).all()
    return plans



@router.post("/api/v1/subscription/checkout/{plan_id}")
async def subscribe_to_a_plan(plan_id:str,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):

    customer = db.query(models.Customer).filter(models.Customer.user_id == user.id).first()
    CUSTOMER_ID = customer.customer_id
    stripe.api_key = os.getenv("STRIPE_API_KEY")

    querr = db.query(models.Subscription).filter(plan_id==plan_id).first()
    plans = querr
    querry = db.query(models.CustomerSubscription).filter(models.CustomerSubscription.user_id == user.id).first()
    subscription_id = querry.subscription_id
    if not user:
        raise HTTPException(status_code=401, detail="please signin")
    else:   
        try:

            sessions = stripe.checkout.Session.create(
                success_url = success_url,
                cancel_url = cancel_url,
                customer=CUSTOMER_ID,
                mode='subscription',
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
            # print(sessions)
            return {"url":sessions['url']}
        except Exception as e:
            return {"status_code": 403, "error": e.args}

        # return {"url":sessions['url']}




@router.patch("/api/v1/subscription/{plan_id}",description="edit plans")
async def Update_a_Subscription_plan(plan_id:int,request: schemas.SubscriptionBase,db:Session = Depends(get_db)):
    plans = db.query(models.Subscription).filter(models.Subscription.id == plan_id)
    plans.update(request.dict(exclude_unset=True))
    db.commit()
    # subscription = stripe.Subscription.retrieve(customer_id)
    return {"Plan updated successfully"}




@router.get("/api/v1/subscription/status")
async def check_subscription_status(db: Session = Depends(get_db),user:dict = Depends(get_current_user)):
    querry = db.query(models.CustomerSubscription).filter(models.CustomerSubscription.user_id == user.id).first() #query customer tables
    profile = db.query(models.User).filter(models.User.id == user.id) #query user to update
    customer_id = querry.subscription_id
    try:
        subscription = stripe.Subscription.retrieve(customer_id)
    except Exception as e:
            return {"status_code": 403, "error": e.args}
    if subscription.status == 'cancelled':
        status = {"code":404,"message":"subscription is cancelled"}
    else:
        # Check if the subscription has expired
        if subscription.current_period_end == datetime.now().timestamp():
            # Cancel the subscription
            subscription.delete()
            print('Subscription has been cancelled')
            status = {"code":405,"message":"subscription has been cancelled"}
            return status
        else:
            print('Subscription is still active or has not yet expired')
            status = {"code":201,"message":"subscription still active"}
            return status
    return status



@router.get('/api/v1/subscription/id',description="list of available plans")
async def get_subscription_plans(db: Session = Depends(get_db)):
    plans = db.query(models.CustomerSubscription).all()
    return plans
