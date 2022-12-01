
import os
from fastapi import APIRouter,status,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..import schemas
from ..dependencies import get_current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

router=APIRouter(tags=['chat'],prefix="/api/v1/chatbot")

@router.post('/')
def chatbot(payload:schemas.ChatBot):
    email = payload.email
    messages = payload.message
