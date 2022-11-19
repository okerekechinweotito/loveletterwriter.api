# from fastapi import APIRouter,Header
# from typing import Union
# #from Love_me_app.util.dto import TrainerValue,TrainerValueUpdate
# # from Love_me_app.business.ai_trainer import AITrainerBusiness
# from sqlalchemy.orm import Session
# from fastapi.params import Depends
# from .. import database 


# router = APIRouter(tags=['ai_trainer'],prefix="/api/v1/ai_trainer")

# # This endpoint is used to return all questions/survey a user needs to answer
# # The answers/values will be used to train the OpenAi model/prompt to generate love letter
# # tailored to the receiver


# @router.get("/")
# async def get_all_ai_trainer(token: Union[str, None] = Header(default=None), db:Session = Depends(get_db), length: int = 10, start: int = 0):
#     api_response = AITrainerBusiness.get_all_trainer(length, start, db)
#     return api_response


# @router.post("/{receiver_id}")
# async def store_trainer_value(receiver_id,item: TrainerValue, token: Union[str, None] = Header(default=None), db:Session = Depends(get_db),):
#     api_response = AITrainerBusiness.store_trainer_value(item,receiver_id,db)
#     return api_response


# @router.put("/{ai_trainer_id}/{receiver_id}")
# async def update_trainer_value(receiver_id, ai_trainer_id, item: TrainerValueUpdate, token: Union[str, None] = Header(default=None), db:Session = Depends(get_db),):
#     api_response = AITrainerBusiness.update_trainer_value(item, ai_trainer_id, receiver_id, db)
#     return api_response


# @router.delete("/{ai_trainer_id}/{receiver_id}")
# async def delete_trainer_value(receiver_id, ai_trainer_id, token: Union[str, None] = Header(default=None),db:Session = Depends(get_db),):
#     api_response = AITrainerBusiness.delete_trainer_value(ai_trainer_id, receiver_id, db)
#     return api_response
