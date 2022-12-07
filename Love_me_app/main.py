from fastapi import FastAPI
from .models import * 
from .database import engine
from fastapi.middleware.cors import CORSMiddleware
from aioprometheus import Counter, MetricsMiddleware
from aioprometheus.asgi.starlette import metrics
from .import models
from .database import engine
from .routers import ai_trainer,authentication,letter,receiver,schedule,subscription,transaction,users,product_review,dashboard,contact_page,mailsubscriber, role_application, feedback, admin, reset, chat_bot
from fastapi.staticfiles import StaticFiles

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
    {
        "name": "reset_password",
        "description": "Operations related to reseting password in the love letter writer app",
    },
    {
        "name": "chat_bot",
        "description": "The Operation related to chat bot",
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

# Any custom application metrics are automatically included in the exposed
# metrics. It is a good idea to attach the metrics to 'app.state' so they
# can easily be accessed in the route handler - as metrics are often
# created in a different module than where they are used.
app.state.users_events_counter = Counter("events", "Number of events.")

#middleware for prometheus
app.add_middleware(MetricsMiddleware)
app.add_route("/metrics", metrics)


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
app.include_router(reset.router)
app.include_router(mailsubscriber.router)
app.include_router(admin.router)
app.include_router(feedback.router)
app.include_router(chat_bot.router)

#StaticFiles Configuration
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
def get():
    return {"msg": "Home page on!"}

