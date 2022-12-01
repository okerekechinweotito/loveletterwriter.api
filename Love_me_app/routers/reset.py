import os
from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..crud import UserCrud
from ..import schemas,models
from ..dependencies import get_current_user
from ..utils import hash_password
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import uuid
from datetime import datetime,timedelta

router=APIRouter(tags=['reset_password'],prefix="/api/v1/reset")

def get_expires_at(minutes:int):
    return (datetime.now() + timedelta(minutes=minutes))


@router.post('/send_reset_email')
def send_reset_email(payload:schemas.PassReset,db:Session = Depends(get_db),):
    email = payload.email
    user = UserCrud.get_user_by_email(db,email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="There is no user with this email")
    token = uuid.uuid4().hex[:6].upper()
    new_token = models.PasswordResetToken(token=token,email=email,expiry_time=get_expires_at(15))
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    
    SMTP_HOST_SENDER = os.getenv("SMTP_HOST_SENDER")

    message = Mail(
    from_email=SMTP_HOST_SENDER,
    to_emails=f"{email}",
    subject=f"Password Reset",
    html_content=f"<p>Here is your reset {token}</p>")
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

@router.post('/validate_token')
def validate_token(payload:schemas.ValidateResetToken,db:Session = Depends(get_db)):
    token = payload.token
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    is_valid = None
    if reset_token:
        if reset_token.expiry_time >= datetime.now():
            is_valid = True
        else:
            is_valid = False
    else:
        is_valid = False
    
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid token")
    
    return {"Token Validated"}

@router.post('/password_reset')
def password_reset(payload:schemas.NewPassword,db:Session = Depends(get_db)):
    new_password = payload.password
    token = payload.token
    reset_token = db.query(models.PasswordResetToken).filter(models.PasswordResetToken.token == token).first()
    email = reset_token.email
    user = UserCrud.get_user_by_email(db,email)
    new_password = hash_password(new_password)
    user.password = new_password
    db.commit()
    return {'Password Reset successful'}

    