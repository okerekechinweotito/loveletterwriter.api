from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi_pagination import Page, paginate, add_pagination
from Love_me_app.database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models


router = APIRouter(tags=["mailsubscribers"], prefix="/api/v1/subscriber")
# add_pagination(router)

@router.post("/")
def register_subscriber(subscriber: schemas.MailSubscriber, db:Session=Depends(get_db)):
    # check if email already exist
    exists_subscriber = db.query(models.MailSubscriber).filter_by(email=subscriber.email).first() is not None
    if exists_subscriber:
        raise HTTPException(status_code=403, detail="You are already subscribed to our mailing list")

    # add new subscriber to the database
    try:
        new_subscriber = models.MailSubscriber(email=subscriber.email)   
        db.add(new_subscriber)
        db.commit()
        db.refresh(new_subscriber)
        return("You have successfully subscribed to our mailing list")
    except:
        db.rollback()
        return ("Something went wrong. Mail subscription not successfully")


@router.get("/")
def get_subscribers(db:Session=Depends(get_db), page_num: int = 1, page_size: int = 20):
    # page size is number of subscribers per page
    start = (page_num - 1) * page_size
    end = start + page_size

    all_subscribers = db.query(models.MailSubscriber).all()
    # return paginated subscribers
    return all_subscribers[start:end]

# add_pagination(router)
