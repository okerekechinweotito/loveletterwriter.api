import os
from fastapi_mail import FastMail, MessageSchema, MessageType
from celery import Celery
from .models import Schedule
from datetime import datetime, timezone
from .models import Schedule
from .database import  SessionLocal
from .send_email import env_config
from dotenv import load_dotenv

load_dotenv()

celery=Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))



@celery.task
def send_letter(letter, email_to):
    body={'letter':letter}
    message = MessageSchema(
    subject='Your Love letter',
    recipients=[email_to],
    template_body=body,
    subtype=MessageType.html,
)
    fm = FastMail(env_config)
    try:
        fm.send_message(message, template_name='love_letter_email.html')
        return True
    except:
        return False




@celery.task
def send_scheduled_letters():
    db=SessionLocal()
    schedules=db.query(Schedule).filter(Schedule.completed== False,Schedule.schedule_time <= datetime.now(tz=timezone.utc)).all()
    if schedules:
        for schedule in schedules:
                send_letter.delay(schedule.letter.letter, schedule.letter.receiver.email)
                schedule.completed=True
                db.commit()
                db.refresh(schedule)
        return True
    else: 
        return False

            


celery.conf.beat_schedule= { 
    'send_sceduled_letters':{ 
        'task': 'Love_me_app.worker.send_scheduled_letters',
        'schedule':120,

    }

}
