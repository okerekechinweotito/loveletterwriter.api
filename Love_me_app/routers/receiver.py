from fastapi import APIRouter,status,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session 
from ..database import get_db
from ..import models,schemas
from typing import List

router = APIRouter(tags=['Receiver'],prefix="/api/v1/receiver")

@router.post('/',response_model= schemas.DisplayReceiver)
def create_receiver(request: schemas.Receiver,db:Session = Depends(get_db)):
    new_receiver = models.Receiver(name=request.name,email=request.email,phone_number=request.phone_number,
                                  user_id=request.user_id)
    db.add(new_receiver)
    db.commit()
    db.refresh(new_receiver)
    return new_receiver

@router.get('/{receiver_id}',response_model=schemas.DisplayReceiver)
def get_receiver(id, response: Response, db:Session = Depends(get_db)):
    receiver = db.query(models.Receiver).filter(models.Receiver.id == id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver not found")
    return receiver

@router.get('/',response_model=List[schemas.DisplayReceiver])
def get_receivers(response: Response, db:Session = Depends(get_db)):
    receivers = db.query(models.Receiver).all()
    return receivers

@router.patch('/{receiver_id}')
def patch_receiver(id, request:schemas.Receiver, db:Session = Depends(get_db)):
    receiver = db.query(models.Receiver).filter(models.Receiver.id == id)
    if not receiver.first():
        pass
    receiver.update(request.dict())
    db.commit()
    return {'Receiver successfully updated'}

@router.delete('/{receiver_id}')
def delete_receiver(id, db:Session = Depends(get_db)):
    db.query(models.Receiver).filter(models.Receiver.id == id).delete(synchronize_session=False)
    db.commit()
    return {"Receiver successfully deleted"}
