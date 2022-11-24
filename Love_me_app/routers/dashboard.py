from fastapi import APIRouter,Depends
from ..dependencies import get_current_user
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models

router = APIRouter(tags=["dashboard"])


@router.get("/api/v1/dashboard")
async def LetterDashbaord(user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    """it return two lists, one is scheduled, the other is sent"""
    #relationship method
    # letter = user.letter
    # schedule = user.schedule
    scheduled = db.query(models.Schedule).filter(models.Schedule.user_id == user.id).all()
    sent = db.query(models.Letter).filter(models.Letter.user_id == user.id).all()
    return {"sent":sent,"scheduled":scheduled}


@router.get("/api/v1/dashboard/scheduled/{id}")
async def Letterdetails(id:int,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    details  = db.query(models.Schedule).filter(models.Schedule.id == id).first()
    return details 



@router.get("/api/v1/dashboard/sent/{id}")
async def Letterdetails(id:int,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    details  = db.query(models.Letter).filter(models.Letter.id == id).first()
    return details 
