from fastapi import FastAPI
from models import * 
from schemas import *
from database import engine,SessionLocal
from routers import ai_trainer,authentication,letter,schedule,subscription,transaction,users

app = FastAPI(
    title="LoveMeApp",
    description="You don't know how to share your deepest feelings? Why not let an AI write love letters for you? Schedule it so it generates love letters and sends to your loved ones weekly for a small fee.",
)
Base.metadata.create_all(engine)

# app.include_router(ai_trainer.router)
# app.include_router(authentication.router)
# app.include_router(letter.router)
# app.include_router(schedule.router)
app.include_router(subscription.router)
# app.include_router(transaction.router)
# app.include_router(users.router)
# db = SessionLocal()
# @app.post("/sub",response_model=Subscription)
# async def subsc(subscription:Subscription):
#     data = Subscription(
#         id = subscription.id,
#         name=subscription.name,
#         description=subscription.description,
#         months=subscription.months,
#         total_sms=subscription.total_sms,
#         amount=subscription.amount,
#         date_created=subscription.date_created
#     )
#     db.add(data)
#     db.commit()


#     return data 
