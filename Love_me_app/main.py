from fastapi import FastAPI
from .models import * 
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from .import models
from .database import engine
from .routers import ai_trainer,authentication,letter,receiver,schedule,subscription,transaction,users,product_review,dashboard,contact_page,mailsubscriber, role_application,admin


tags_metadata = [
    {
        "name": "auth",
        "description": "Operations related to the everything auth",
    },
    {
        "name": "ai_trainer",
        "description": "Operations related to the survey questions to be answered for each love letter receiver. Used in the openai prompt",
    },
    {
        "name": "subscription",
        "description": "Operations related to the subscription plans  and co",
    },
    {
        "name": "transactions",
        "description": "Operations related to the transaction and verification of payment",
    },
    {
        "name": "receiver",
        "description": "Operations related to the receiver of the love letters",
    },
      {
        "name": "contact",
        "description": "The Operation related to our contact page in the love letter writer app",
    },
]

app = FastAPI(
    title="LoveMeApp",
    description="You don't know how to share your deepest feelings? Why not let an AI write love letters for you? Schedule it so it generates love letters and sends to your loved ones weekly for a small fee.",
    openapi_tags=tags_metadata
)
Base.metadata.create_all(engine)
app.add_middleware(CORSMiddleware,
allow_origins=['*'],
allow_credentials=True,
allow_methods=['*'],
allow_headers=['*'])


app.include_router(authentication.router)
app.include_router(ai_trainer.router)
app.include_router(letter.router)
app.include_router(receiver.router)
app.include_router(schedule.router)
app.include_router(subscription.router)
app.include_router(transaction.router)
app.include_router(users.router)
app.include_router(contact_page.router)
app.include_router(dashboard.router)
app.include_router(product_review.router)
app.include_router(role_application.router)
app.include_router(mailsubscriber.router)
app.include_router(admin.router)

@app.get("/")
def get():
    return {"msg": "Home page on!"}

