from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
from .. import schemas

# initialize router

router = APIRouter(tags=['chat_bot'], prefix="/api/v1/chat")


@router.post("/")
async def chat_with_ai(item: schemas.ChatBot, user: dict = Depends(get_current_user), db: Session = Depends(get_db), ):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please log in")
    user_id = user.id
    # api_response = LetterBusiness.generate_custom_letter(user_id, item, db)
    return {}
