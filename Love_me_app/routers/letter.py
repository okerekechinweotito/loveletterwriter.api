"""sent_letters = []
scheduled_letters = []
letters = db.query(models.Letter).join(models.Schedule).all()
for letter in letters:
    if Schedule.schedule_time > datetime.now():
        schedule_letters.append(letter)
    else:
        sent_letters.append(letter)


"""
from ..dependencies import get_current_user
from fastapi import Depends, APIRouter, HTTPException
from .. import schemas, models
from ..database import get_db
from sqlalchemy.orm import Session 

# initialize router
router = APIRouter(prefix="/api/v1/letter")
db = get_db()

# function to get all letters
@router.get("/")
async def get_all_letter(user:dict = Depends(get_current_user), db:Session=Depends(get_db)):
    sent_letters = []
    scheduled_letters = []
    # raise a user not found error if user details is not correct
    if not user :
        raise HTTPException(status_code=401, detail="User not Found") 
    # get all user letters from the database
    letters = db.query(models.Letter).filter(models.Letter.user_id).all()
    return letters
    
@router.get("/sent")
def get_sent_letter(user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    # sent_letters = []
    if user:
        sent_letters = db.query(models.Letter).filter(is_sent=True).all()
        # if models.Letter.is_sent == True:

        # for letter in letters:
        #     sent_letters.append(letter)
        return sent_letters
    else:
        raise HTTPException(status_code=401, detail="User not Found")


@router.get("/scheduled")
def get_scheduled_letter(user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    # sent_letters = []
    if user:
        # get all scheduled_letters in the db 
        scheduled_letters = db.query(models.Letter).filter(models.Letter.user_id).filter(is_scheduled=True).all()
        return scheduled_letters
    else:
        raise HTTPException(status_code=401, detail="User not Found")


