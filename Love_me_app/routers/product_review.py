from fastapi import APIRouter,HTTPException,status
from sqlalchemy.orm import Session
from Love_me_app.database import get_db
from fastapi import Depends
from ..dependencies import get_current_user
from ..schemas import ProductReviews,PydanticReview
from ..models import ProductReview as ProductReviewModel
from fastapi_paginate import Page, add_pagination, paginate
from datetime import datetime
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

    reviews = db.query(ProductReviewModel).all()
    for review in reviews:
        review.user
        print(review.user)
        
    return reviews





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