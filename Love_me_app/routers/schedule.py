from fastapi import APIRouter, Body, Depends, HTTPException
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..dependencies import get_current_user
from datetime import datetime
from .. import schemas
from typing import List
router=APIRouter(tags=['Schedule'])




def get_object_or_404(db,model, id, user):
    obj=db.query(model).filter(model.id==id, model.user_id ==user).first()
    if not obj:
        raise HTTPException(detail='this schedule does not exists', status_code=404)
    return obj
    

@router.post('/schedule-letter/{letter_id}', summary='endpoint to schedule letters')
def schedule_letter(letter_id:int,user:dict=Depends(get_current_user),db:Session=Depends(get_db), date_scheduled:datetime=Body()):
    obj=db.query(models.Letter).filter(models.Letter.id==letter_id, models.Letter.user_id ==user.id).first()
    if not obj:
        raise HTTPException(detail='this letter does not exists', status_code=404)
    schedule=models.Schedule(user_id=user.id, letter_id=letter_id, schedule_time=date_scheduled)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return {'message':'letter has been scheduled'}

@router.get('/schedule/{schedule_id}', response_model=schemas.Schedule_Letter, summary='endpoint to get a particular schedule')
def get_schedule(schedule_id:int, db:Session=Depends(get_db), user:dict=Depends(get_current_user)):
    schedule=get_object_or_404(model=models.Schedule, db=db, user=user.id, id=schedule_id)
    return schedule


@router.get('/schedule', response_model=List[schemas.Schedule_Letter], summary='endpoint to get all active scheduled letters')
def get_all_scheduled_letter(offset:int=0, limit:int=10,db:Session=Depends(get_db), user:dict=Depends(get_current_user)):
    letters=db.query(models.Schedule).filter(models.Schedule.completed==False, models.Schedule.user_id==user.id).offset(offset).limit(limit).all()
    return letters


@router.patch('/schedule/{schedule_id}/', status_code=200, response_model=schemas.Schedule_Letter, summary='endpoint to update schedule time')
def update_scedule( schedule_id:int,db:Session=Depends(get_db), date_scheduled:datetime=Body(), user:dict=Depends(get_current_user)):
    schedule=get_object_or_404(model=models.Schedule, db=db, user=user.id, id=schedule_id)
    schedule.schedule_time= date_scheduled
    db.commit()
    db.refresh(schedule)
    return schedule

@router.delete('/schedule/{schedule_id}/', status_code=204,  summary='endpoint to delete schedule')
def delete_schedule(schedule_id:int,db:Session=Depends(get_db), user:dict=Depends(get_current_user)):
    schedule=get_object_or_404(model=models.Schedule, db=db, user=user.id, id=schedule_id)
    db.delete(schedule)
    db.commit()
    return {'message':'sucessfully deleted'}








    

