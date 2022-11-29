from fastapi import APIRouter, Depends, HTTPException, status
from Love_me_app.database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models


router = APIRouter(tags=["mailsubscribers"], prefix="/api/v1/subscriber")

@router.post("/")
async def subscriber(subscriber: schemas.MailSubscriber, db:Session=Depends(get_db)):
    # check if email already exist
    exists_subscriber = db.query(models.MailSubscriber).filter_by(email=subscriber.email).first() is not None
    if exists_subscriber:
        raise HTTPException(status_code=403, detail="You are already subscribed to our mailing list")

    # add new subscriber to the database
    new_subscriber = models.MailSubscriber(email=subscriber.email)   
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    return("You have successfully subscribed to our mailing list")


@router.get("/")
async def get_subscribers(db:Session=Depends(get_db)):
    all_subscribers = db.query(models.MailSubscriber).all()
    return all_subscribers

