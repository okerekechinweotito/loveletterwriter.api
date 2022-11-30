import os
from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..import schemas
from ..dependencies import get_current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

router=APIRouter(tags=['contact'],prefix="/api/v1/contact_us")

@router.post('/')
def contact_us(payload:schemas.ContactUs, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    name=payload.name
    email=payload.email
    messages=payload.messages

    SMTP_HOST_SENDER = os.getenv('SMTP_HOST_SENDER')

    message = Mail(
    from_email=SMTP_HOST_SENDER,
    to_emails="contact.lovemeapp@gmail.com",
    subject="User Enquiry",
    html_content=f"<p>This email is from {name} with the email address,{email}</p><p>{messages}</p>")
    try:
        SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') 
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return {'Sent successfully'}