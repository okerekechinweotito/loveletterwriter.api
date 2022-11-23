from fastapi import APIRouter,HTTPException,status
from Love_me_app.business.letter import LetterBusiness
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
import smtplib

router = APIRouter(tags=['product_review'],prefix="/api/v1/review")


@router.post('/')
def create_review():

    pass



@router.get('/')
def get_reviews():
    pass


@router.patch('/')
async def update_review():
    pass


