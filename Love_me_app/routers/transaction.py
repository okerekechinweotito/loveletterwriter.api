from fastapi import APIRouter,Depends,Request,Header
from datetime import timedelta
from fastapi.responses import Response
import stripe



router = APIRouter(tags=['transactions'])



@router.post("/completed",description="transaction webhook")
async def completed(requests:Request,stripe_signature:str = Header(str)):
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
    if event.type == 'checkout.session.completed':
        # user.is_sub_active = True
        # user.sub_end_date = timedelta(days=30)
        payment_intent = event.data # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!',payment_intent)
        details = {
            'user_name':event.data.metadata.user_name,
            'user_email':event.data.metadata.user_email,
            'user_id':event.data.metadata.user_id,
            'plan_type':event.data.metadata.plan_type,
            'month':event.data.metadata.month,
            'total_sms':event.data.metadata.totel_sms
        }
        print(details)

    print('Handled event type {}'.format(event['type']))
    


# def verify_payment():
#     completed()


