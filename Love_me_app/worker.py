import os
from fastapi_mail import FastMail, MessageSchema
from celery import Celery
from .models import Schedule
from datetime import datetime, timezone, timedelta 
from .models import Schedule, Letter
from .database import  SessionLocal
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv
import asyncio


load_dotenv()

celery=Celery(__name__, broker=os.getenv('CELERY_BROKER_URL', None))
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

env_config = ConnectionConfig(
   MAIL_USERNAME='contact.lovemeapp@gmail.com',
    MAIL_PASSWORD=os.getenv('MAIL2_PASSWORD'),
    MAIL_FROM='contact.lovemeapp@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='LoveMe',
    USE_CREDENTIALS=True,
    MAIL_TLS=True,
    MAIL_SSL=False,
    TEMPLATE_FOLDER='templates',
 )

async def send_email(user, letter, recepient):


    message=MessageSchema(
        subject=f'Love letter from {user}',
        recipients=[recepient,],
        template_body={'user':user, 'letter':letter.split('\n\n')},
        subtype='html'

    )
    f=FastMail(env_config)
    try:
        await f.send_message(message, template_name='letter.html')
    except:
        return 'working'

@celery.task
def send_letter(user, letter, recepient, id):
    try:
        asyncio.run(send_email(user, letter, recepient))
        db=SessionLocal()
        letter=db.query(Letter).filter(Letter.id==id).first()
        letter.date_sent=datetime.now(tz=timezone.utc)
        db.commit()
        db.refresh(letter)
        return f'letter sent-- id: {id}  {recepient}'
    except Exception as e:
        return f'letter failed to send-- id: {id}   {e}'



@celery.task
def send_scheduled_letters():
    db=SessionLocal()
    schedules=db.query(Schedule).filter(Schedule.completed== False,Schedule.schedule_time <= datetime.now(tz=timezone.utc)+timedelta(hours=1)).all()
    if schedules:
        for schedule in schedules:
                send_letter.delay(f"{schedule.user.first_name} {schedule.user.last_name}", schedule.letter.letter, schedule.letter.receiver.email, schedule.letter.id)
                schedule.completed=True
                db.commit()
                db.refresh(schedule)
        return 'Scheduled letters available'
    else: 
        return 'No scheduled letters'

            


celery.conf.beat_schedule= { 
    'send_sceduled_letters':{ 
        'task': 'Love_me_app.worker.send_scheduled_letters',
        'schedule':60,

    }

}
