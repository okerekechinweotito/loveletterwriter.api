from fastapi import APIRouter,HTTPException,status
from Love_me_app.business.letter import LetterBusiness
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user


router = APIRouter(tags=['letter'],prefix="/api/v1/letter")


@router.post("/{receiver_id}")
async def generate_letter(receiver_id,user:dict=Depends(get_current_user), db:Session = Depends(get_db),):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Please log in")
    user_id = user.id
    api_response = LetterBusiness.generate_letter(user_id, receiver_id,db)
    return api_response
