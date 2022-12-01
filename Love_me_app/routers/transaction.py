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
    endpoint_secret = os.getenv("ENDPOINT_SECRET")
    

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

        customer = event.data.object.customer
        
        cus_profile = db.query(models.Customer).filter(models.Customer.customer_id==customer).first()

        profile = db.query(models.User).filter(models.User.id == cus_profile.user_id).first()
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


@router.post("/api/v1/transaction/create-customer/")
async def create_customer_object(user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
    if user:
        CUSTOMER_EMAIL = user.email
        CUSTOMER_NAME = f'{user.first_name}  {user.last_name}'
        try:
            # create customer_id for the current user
            customer = stripe.Customer.create(
                email=CUSTOMER_EMAIL,
                name=CUSTOMER_NAME,
            )
            insert_id = models.Customer(user_id=user.id, customer_id=customer['id'])
            db.add(insert_id)
            db.commit()
            db.refresh(insert_id)

            return {"Customer_id": customer['id']}

        except Exception as e:
            return {"status_code": 403, "error": e.args}
   
    return HTTPException(status_code=401, detail="Please Login")



@router.post("/api/v1/transaction/create-subscription/")
async def create_subscription_object(user:dict = Depends(get_current_user),db: Session = Depends(get_db)):
    if user:

        id = user.id
        users = db.query(models.Customer).filter(models.Customer.user_id == id).first()
        CUSTOMER_ID = users.customer_id

        try:
            subscription = stripe.Subscription.create(
                    customer=CUSTOMER_ID,
                    items=[{
                        "price": os.getenv("SWEET_PLAN_ID")
                    }],
                    payment_behavior="default_incomplete",
                    payment_settings={"save_default_payment_method": "on_subscription"},
                    expand=["latest_invoice.payment_intent"]
            )
            insert_sub = models.CustomerSubscription(user_id=id, subscription_id=subscription.id)
            db.add(insert_sub)
            db.commit()
            db.refresh(insert_sub)
            print(subscription)

            return {
                    "subscriptionId": subscription.id, "clientSecret": subscription.latest_invoice.payment_intent.client_secret
            }

        except Exception as e:
            return {"statusCode": 403, "error": e.args }
    return {"please login"}


@router.post('/api/v1/transaction/customer-portal/', tags=["Customer"],)
async def customer_portal( user:dict=Depends(get_current_user),db: Session = Depends(get_db)):
    if user:
        id = user.id
        users = db.query(models.Customer).filter(models.Customer.user_id == id).first()
        CUSTOMER_ID = users.customer_id

        try:
            session = stripe.billing_portal.Session.create(
                customer=CUSTOMER_ID,
                return_url='https://loveme.hng.tech'
            )
            return {"status_code": 303, "Session_url(note: user is redirected to this url)": session.url}

        except Exception as e:
                return{"status_Code": 200, "errors": e.args}

    return HTTPException(status_Code=401, detail="invalid request")
