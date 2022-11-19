from fastapi import APIRouter,Depends,Request
import  schemas 
from dependencies import get_current_user
from fastapi.responses import Response,RedirectResponse
from sqlalchemy.orm import Session
import models
import json
from database import get_db
from datetime import timedelta
import stripe 



router = APIRouter(tags=['subscription'])


@router.post("/api/v1/subscription",description="endpoint to post subscription")
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


@router.get('/api/v1/subscription/plans',description="list of available plans")
async def SubscriptionPlans(db: Session = Depends(get_db)):
    plans = db.query(models.Subscription).all()
    return plans





@router.post("/api/v1/subscription/checkout/{plan_id}")
async def subscribe_plan(plan_id:int,db: Session = Depends(get_db),user:dict = Depends(get_current_user)):

    stripe.api_key = 'sk_test_51M5T6WGYYMC7FKsItosehAJ1CJGFajEiYBLYNTty6sGgpNfqjukMbir08BUcLVzOLzpnSrFY0x1oOO2NozpsSZDI00GUJdvY6u'

    querr = db.query(models.Subscription).filter_by(id=plan_id).first()
    plans = querr

    if plans.name == "sweet love":

        sessions = stripe.checkout.Session.create(
            success_url = "http://127.0.0.1:8000/completed?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = 'http://127.0.0.1:8000/docs',
            mode='subscription',
            metadata = {
                'user_id':user.id,
                'user_name':user.first_name,
                'user_email':user.email,
                'plan_type':plans.name,
                'month':plans.months,
                'total_sms':plans.total_sms
            },
            payment_method_types =["card"],
                line_items =[{
                    'price':'price_1M5TfuGYYMC7FKsIAO8k3YN2',
                    'quantity':1,
                }
                ]
            )
    elif plans.name == "Advanced":
        sessions = stripe.checkout.Session.create(
            success_url = "http://127.0.0.1:8000/completed?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = 'http://127.0.0.1:8000/docs',
            mode='subscription',
             metadata = {
                'user_id':user.id,
                'user_name':user.first_name,
                'user_email':user.email,
                'plan_type':plans.name,
                'month':plans.months,
                'total_sms':plans.total_sms
            },
            payment_method_types =["card"],
                line_items =[{
                    'price':'price_1M5ThaGYYMC7FKsIYViZMmtm',
                    'quantity':1,
                }
                ]
            )
    elif plans.name == "Pro gratifying":
        sessions = stripe.checkout.Session.create(
            success_url = "http://127.0.0.1:8000/completed?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = 'http://127.0.0.1:8000/docs',
            mode='subscription',
             metadata = {
                'user_id':user.id,
                'user_name':user.first_name,
                'user_email':user.email,
                'plan_type':plans.name,
                'month':plans.months,
                'total_sms':plans.total_sms
            },
            payment_method_types =["card"],
                line_items =[{
                    'price':'price_1M5TiIGYYMC7FKsITCqacRIS',
                    'quantity':1,
                }
                ]
            )

    return {"url":sessions['url'],
        "checkout_id":sessions['id']}




