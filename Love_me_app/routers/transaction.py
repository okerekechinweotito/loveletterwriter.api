from fastapi import APIRouter,Depends,Request,Header,HTTPException
from sqlalchemy.orm import Session
from dateutil.relativedelta import relativedelta
from ..import models
from ..dependencies import get_current_user
import stripe
from dotenv import load_dotenv
import os 
load_dotenv()
from datetime import datetime
from ..database import get_db
 
from sqlalchemy.orm import Session



router = APIRouter(tags=['transactions'])
stripe.api_key = os.getenv("STRIPE_API_KEY")


@router.post("/completed",description="transaction webhook")
async def completed(requests:Request,stripe_signature:str = Header(), db:Session = Depends(get_db)):
 
    payload =await requests.body()
    sig_header = stripe_signature
    # endpoint_secret = os.getenv("ENDPOINT_SECRET")
    endpoint_secret = 'whsec_9408e100f9b71cae7e32ce9f54927bb1f2f76a88dfe62d9793e5d0ce16617066'
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e
    if event['type'] == 'checkout.session.completed':
        data = models.Transaction(
            user_id = event.data.object.metadata.user_id,
            ref_no = event.data.object.id,
            date_created = datetime.utcfromtimestamp(int(event.data.object.created)).strftime('%Y-%m-%d %H:%M:%S')
        )
        object_id = int(event.data.object.metadata.user_id)
        end = event.data.object.metadata.month
        profile = db.query(models.User).filter(models.User.id==object_id).first()
        end_date = datetime.now() + relativedelta(months=int(end))
        profile.is_sub_active = True
        profile.sub_end_date = end_date
        profile.plan_type = event.data.object.metadata.plan_type
        profile.free_trial = False 
        db.add(data)
        try:
            db.commit()
        except Exception as e:
            print(str(e))
        print("saved to data base..........................................")
        
    elif event['type'] == 'customer.subscription.deleted':

        """this here checks if sub is expired and updates user's records accordingly"""

        email = event.data.object.email
        profile = db.query(models.User).filter(models.User.email==email).first()
        profile.is_sub_active = False
        profile.sub_end_date = None
        try:
            db.commit()
        except Exception as e:
            print(str(e))
        print("saved to data base..........................................")

    print('Handled event type {}'.format(event['type']))
    


# def verify_payment():
#     completed()

@router.get("/transactions",description="get all the transaction in the db")
async def transactions_data(db: Session = Depends(get_db)):
    plans = db.query(models.Transaction).all()
    return plans
