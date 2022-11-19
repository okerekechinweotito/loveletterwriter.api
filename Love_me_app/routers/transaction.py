from fastapi import APIRouter,Depends,Request
from datetime import timedelta
from fastapi.responses import Response
import stripe



router = APIRouter(tags=['transactions'])



@router.post("/completed",description="transaction webhook")
async def completed(requests:Request):
    payload = requests.body
    sig_header = requests.headers.get('STRIPE_SIGNATURE')
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
    if event.type == 'payment_intent.succeeded':
        print(event['metadata']['email'])
        # user.is_sub_active = True
        # user.sub_end_date = timedelta(days=30)
        # payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    print('Handled event type {}'.format(event['type']))

    return Response(success=True)

