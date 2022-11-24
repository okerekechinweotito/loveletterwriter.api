
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()
 
class Environ:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')
    TEMPLATE_FOLDER = os.getenv('TEMPLATE_FOLDER')
    TEMPLATE_NAME = os.getenv('TEMPLATE_NAME')


env_config = ConnectionConfig(
    MAIL_USERNAME=Environ.MAIL_USERNAME,
    MAIL_PASSWORD=Environ.MAIL_PASSWORD,
    MAIL_FROM=Environ.MAIL_FROM,
    MAIL_PORT=Environ.MAIL_PORT,
    MAIL_SERVER=Environ.MAIL_SERVER,
    MAIL_FROM_NAME=Environ.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Environ.TEMPLATE_FOLDER
 )



async def password_reset_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    
    fm = FastMail(env_config)
    await fm.send_message(message, template_name=Environ.TEMPLATE_NAME)

