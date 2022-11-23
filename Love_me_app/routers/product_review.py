from fastapi import APIRouter,HTTPException,status
from Love_me_app.business.letter import LetterBusiness
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
from ..schemas import ProductReviews
from ..models import ProductReview as ProductReviewModel
router = APIRouter(tags=['product_review'],prefix="/api/v1/review")


@router.post('/')
def create_review(productReview: ProductReviews, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    current_user = user

    if current_user is not None:
        review = ProductReviewModel(user=user.id, review=productReview.review)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")


  



@router.get('/all')
def get_reviews( user:dict=Depends(get_current_user), db:Session = Depends(get_db)):

    current_user = user
    if current_user is not None:
        pass



 





