import os
from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..import models 
from ..import schemas
from ..dependencies import get_current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


router=APIRouter(tags=['feedback'],prefix="/api/v1/feedback")

@router.post('/')
async def feedback(payload:schemas.Feedback,  db:Session = Depends(get_db)):
    
    data = models.Feedback(
        is_helpfull = payload.is_helpfull, feedback= payload.feedback)

    db.add(data)
    db.commit()


    SMTP_HOST_SENDER = os.getenv('SMTP_HOST_SENDER')

    message = Mail(
    from_email=SMTP_HOST_SENDER,
    to_emails="contact.lovemeapp@gmail.com",
    subject="Feedback",
    html_content=f"<p>{payload.feedback}</p>")
    try:
        SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') 
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
    return {'Sent successfully'}

@router.get("/api/v1/feedback")
async def Responsefeedback( db:Session = Depends(get_db)):
    details  = db.query(models.Feedback).all()
    return details