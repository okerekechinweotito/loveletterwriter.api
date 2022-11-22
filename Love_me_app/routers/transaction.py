from fastapi import APIRouter,Depends,Request,Header
from sqlalchemy.orm import Session
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from ..import models
from ..dependencies import get_current_user
import stripe
from datetime import datetime
from ..database import get_db
 
from sqlalchemy.orm import Session



router = APIRouter(tags=['transactions'])



@router.post("/completed",description="transaction webhook")
async def completed(requests:Request,stripe_signature:str = Header(),user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    payload =await requests.body()
    sig_header = stripe_signature
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
        # user.is_sub_active = True
        # user.sub_end_date = timedelta(days=30)
        payment_intent = event.data # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!',payment_intent)
        details = {
            'user_name':event.data.object.metadata.user_name,
            'user_email':event.data.object.metadata.user_email,
            'user_id':event.data.object.metadata.user_id,
            'plan_type':event.data.object.metadata.plan_type,
            'month':event.data.object.metadata.month,
        }
        # data = models.Transaction(
        #     user_id = event.data.object.metadata.user_id,
        #     ref_no = event.data.object.id,
        #     date_created = datetime(datetime.utcfromtimestamp(event.data.object.created).strftime('%Y-%m-%d %H:%M:%S'))
        # )
        id = int(event.data.object.metadata.user_id)
        profile = db.query(models.User).filter_by(id=id).first()
        end = event.data.object.metadata.month
        end_date = profile.sub_end_date + relativedelta(months=int(end))

        profile.update(is_sub_active=True,sub_end_date=end_date)
        db.commit()
        # db.add(data)
        # db.commit()
        print("saved to data base..........................................")

    print('Handled event type {}'.format(event['type']))
    


# def verify_payment():
#     completed()

@router.get("/sub")
async def subsc(db: Session = Depends(get_db)):
    plans = db.query(models.Transaction).all()
    return plans
