import os
from celery import Celery
from .models import Schedule
from datetime import datetime, timezone
from .models import Schedule, Letter
from .database import  SessionLocal
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv



load_dotenv()

celery=Celery(__name__, broker=os.getenv('CELERY_BROKER_URL', None))


def send_email(user, letter, recepient):

     
    SMTP_HOST_SENDER ='simeoneumoh@gmail.com'

    message = Mail(
    from_email=SMTP_HOST_SENDER,
    to_emails=f"{recepient}",
    subject=f"Letter from {user}",
    html_content=f"<p>{letter}</p>")
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY') 
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response.body
@celery.task
def send_letter(user, letter, recepient, id):
    try:
        send_email(user, letter, recepient)
        db=SessionLocal()
        letter=db.query(Letter).filter(Letter.id==id).first()
        letter.date_sent=datetime.now(tz=timezone.utc)
        db.commit()
        db.refresh(letter)
        return f'letter sent-- id: {id}'
    except:
        return f'letter failed to send-- id: {id}'



@celery.task
def send_scheduled_letters():
    db=SessionLocal()
    schedules=db.query(Schedule).filter(Schedule.completed== False,Schedule.schedule_time <= datetime.now(tz=timezone.utc)).all()
    if schedules:
        for schedule in schedules:
                send_letter.delay(schedule.letter.receiver.name, schedule.letter.letter, schedule.letter.receiver.email, schedule.letter.id)
                schedule.completed=True
                db.commit()
                db.refresh(schedule)
        return 'Scheduled letters available'
    else: 
        return 'No scheduled letters'

            


celery.conf.beat_schedule= { 
    'send_sceduled_letters':{ 
        'task': 'Love_me_app.worker.send_scheduled_letters',
        'schedule':120,

    }

}
