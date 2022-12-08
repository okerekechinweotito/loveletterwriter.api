from fastapi import APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy import func
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
from ..schemas import ProductReviews
from ..models import ProductReview as ProductReviewModel

from datetime import datetime
from ..models import User
router = APIRouter(tags=['product_review'],prefix="/review")


@router.post('/')
def create_review(productReview: ProductReviews, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    current_user = user
    
    productReviewObj = productReview.dict()
    print(productReviewObj)
    if current_user is not None:
        review = ProductReviewModel(
            user=current_user, 
            review=productReviewObj['review'],
            )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")


  

@router.get('/all')
def get_reviews( db:Session = Depends(get_db)):
    reviews = (
        db.query(ProductReviewModel, User)
        .join(User, ProductReviewModel.user_id == User.id).order_by(func.random()).limit(10)
        .all()
    )
    

    return [
        {
            "id": review.ProductReview.id,
            "review": review.ProductReview.review,
            "date_created": review.ProductReview.date_created,
            "user_id": review.ProductReview.user_id,
            "first_name": review.User.first_name,
            "last_name": review.User.last_name,
            "image": review.User.image,
        }
        for review in reviews
    ]


@router.delete('/{review_id}')
def delete_review(review_id, user:dict=Depends(get_current_user), db:Session = Depends(get_db)):
    current_user = user
    if current_user is not None:
        review = db.query(ProductReviewModel).filter(ProductReviewModel.id==review_id).first()
  
        if review is not None:
            
            db.delete(review)
            db.commit()
            return {"Review  deleted"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")

    




'''
todo:
Add pagination,

User model divide into User and profile

'''

# @router.get('/all',response_model=Page[PydanticReview])
# def get_reviews( db:Session = Depends(get_db)):
# 
    # reviews = db.query(ProductReviewModel).all()
    # for review in reviews:
        # review.user
        # print(review.user)
        # 
    # return paginate(reviews)
# 
# 
# add_pagination(router)
