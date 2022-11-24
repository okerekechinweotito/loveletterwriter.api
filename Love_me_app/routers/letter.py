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
    # raise a user not found error if user details is not correct
    if not user :
        raise HTTPException(status_code=401, detail="User not Found") 
    # get all user letters from the database
    letters = db.query(models.Letter).filter(models.Letter.user_id).order_by(models.Letter.date_created).all()
    return letters
    
@router.get("/sent")
def get_sent_letter(user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    sent_letters = []
    if user:
        # get all sent letters from database
        letters = db.query(models.Letter).filter(models.Letter.user_id).filter(models.Letter.date_sent).order_by(models.Letter.date_sent).all()
        for letter in letters:
            # loop through eachother to check if date sent is not null
            if letter.date_sent != None:
                letter.append(sent_letters)
        return sent_letters

    else:
        raise HTTPException(status_code=401, detail="User not Found")



