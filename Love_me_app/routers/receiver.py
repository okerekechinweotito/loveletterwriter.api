from fastapi import APIRouter,status,Response,HTTPException,Cookie, Request
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..import models,schemas
from ..dependencies import get_current_user
from typing import List
from fastapi_jwt_auth import AuthJWT

router = APIRouter(tags=['receiver'],prefix="/api/v1/receiver")

@router.post('/{letter_id}/',response_model= schemas.DisplayReceiver)
def create_receiver(payload: schemas.Receiver,letter_id:int, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    obj=db.query(models.Letter).filter(models.Letter.id==letter_id, models.Letter.user_id ==user.id).first()
    if not obj:
        raise HTTPException(detail='this letter does not exists', status_code=404)

    new_receiver = models.Receiver(name=payload.name,email=payload.email,phone_number='pop',
                                  user_id=user.id)
    db.add(new_receiver)
    db.commit()
    db.refresh(new_receiver)
    obj.receiver_id=new_receiver.id
    db.commit()
    db.refresh(obj)
    return new_receiver

@router.post('/{letter_id}/{receiver_id}',response_model= schemas.DisplayReceiver)
def use_old_receiver(letter_id:int, receiver_id:int,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    letter=db.query(models.Letter).filter(models.Letter.id==letter_id, models.Letter.user_id ==user.id).first()
    receiver=db.query(models.Receiver).filter(models.Receiver.id==receiver_id, models.Receiver.user_id ==user.id).first()
    if not letter:
        raise HTTPException(detail='this letter does not exists', status_code=404)
    if not receiver:
                raise HTTPException(detail='this receiver does not exists', status_code=404)
    letter.receiver_id=receiver_id
    db.commit()
    db.refresh(letter)
    return receiver



@router.get('/{receiver_id}',response_model=schemas.DisplayReceiver)
def get_receiver(id, response: Response,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    receiver = db.query(models.Receiver).filter(models.Receiver.id == id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver not found")
    return receiver

@router.get('/',response_model=List[schemas.DisplayReceiver])
def get_receivers(response: Response,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    receivers = db.query(models.Receiver).all()
    return receivers

@router.patch('/{receiver_id}')
def patch_receiver(id, request:schemas.Receiver,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    receiver = db.query(models.Receiver).filter(models.Receiver.id == id)
    if not receiver.first():
        pass
    receiver.update(request.dict())
    db.commit()
    return {'Receiver successfully updated'}

@router.delete('/{receiver_id}')
def delete_receiver(id,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    user = user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    db.query(models.Receiver).filter(models.Receiver.id == id).delete(synchronize_session=False)
    db.commit()
    return {"Receiver successfully deleted"}