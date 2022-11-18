from fastapi import FastAPI
from .import models
from .database import engine
from .routers import ai_trainer,authentication,letter,receiver,schedule,subscription,transaction,users

app = FastAPI(
    title="LoveMeApp",
    description="You don't know how to share your deepest feelings? Why not let an AI write love letters for you? Schedule it so it generates love letters and sends to your loved ones weekly for a small fee.",
)
models.Base.metadata.create_all(engine)

# app.include_router(ai_trainer.router)
# app.include_router(authentication.router)
# app.include_router(letter.router)
app.include_router(receiver.router)
# app.include_router(schedule.router)
# app.include_router(subscription.router)
# app.include_router(transaction.router)
# app.include_router(users.router)