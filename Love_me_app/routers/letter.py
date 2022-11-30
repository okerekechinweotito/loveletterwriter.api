import os
from fastapi import APIRouter,HTTPException,status
from Love_me_app.business.letter import LetterBusiness
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
from ..import schemas,models
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# initialize router

router = APIRouter(tags=['letter'],prefix="/api/v1/letter")


# function to get all letters
@router.post("/{receiver_id}")
async def generate_letter(receiver_id,user:dict=Depends(get_current_user), db:Session = Depends(get_db),):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    user_id = user.id
    if user.is_sub_ractive == True:
        api_response = LetterBusiness.generate_letter(user_id, receiver_id,db)
    else:
        if user.free_trial == True:
            api_response = LetterBusiness.generate_letter(user_id, receiver_id,db)
            user.free_trial = False
            db.commit()
        else:
            api_response = {
                    'status': 0,
                    'message': 'Please subscribe to be able to generate letter'
                }
    return api_response


@router.post("/")
async def generate_custom_letter(item: schemas.GenerateLetter, user:dict=Depends(get_current_user), db:Session = Depends(get_db),):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in")
    user_id = user.id
    if user.is_sub_ractive == True:
        api_response = LetterBusiness.generate_custom_letter(user_id, item, db)
    else:
        if user.free_trial == True:
            api_response = LetterBusiness.generate_custom_letter(user_id, item, db)
            user.free_trial = False
            db.commit()
        else:
            api_response = {
                'status': 0,
                'message': 'Please subscribe to be able to generate letter'
            }
    return api_response


@router.get("/")
async def get_all_letter(user:dict = Depends(get_current_user), db:Session=Depends(get_db)):
    # raise a user not found error if user details is not correct
    if not user :
        raise HTTPException(status_code=401, detail="User not Found") 
    # get all user letters from the database
    letters = db.query(models.Letter).order_by(models.Letter.date_created).all()
    return letters
    

@router.get("/sent")
def get_sent_letter(user:dict=Depends(get_current_user), db:Session=Depends(get_db)):
    sent_letters = []
    if user:
        # get all sent letters from database
        letters = db.query(models.Letter).all()
        for letter in letters:
            # loop through eachother to check if date sent is not null
            if letter.date_sent != None:
                sent_letters.append(letter)
            return sent_letters

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")




@router.post("/send/{receiver_id}")
def send_letter(payload:schemas.SendLetter,receiver_id,user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    letter=payload.letter
    user_name = user.first_name
    receiver = db.query(models.Receiver).filter(models.Receiver.id == receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver does not exist")
    receiver_email = receiver.email

    SMTP_HOST_SENDER ='simeoneumoh@gmail.com'

    message = Mail(
    from_email=SMTP_HOST_SENDER,
    to_emails=f"{receiver_email}",
    subject=f"Letter from {user_name}",
    html_content=f"<p>{letter}</p>")
    try:
        SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') 
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    return {'Sent successfully'}