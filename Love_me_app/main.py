from fastapi import FastAPI
from .import models
from .database import engine
from .routers import ai_trainer,authentication,letter,receiver,schedule,subscription,transaction,users

tags_metadata = [
    {
        "name": "ai_trainer",
        "description": "Operations related to the survey questions to be answered for each love letter receiver. Used in the openai prompt",
    },
]

app = FastAPI(
    title="LoveMeApp",
    description="You don't know how to share your deepest feelings? Why not let an AI write love letters for you? Schedule it so it generates love letters and sends to your loved ones weekly for a small fee.",
    openapi_tags=tags_metadata
)
models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(ai_trainer.router)
# app.include_router(letter.router)
app.include_router(receiver.router)
# app.include_router(schedule.router)
# app.include_router(subscription.router)
# app.include_router(transaction.router)
# app.include_router(users.router)