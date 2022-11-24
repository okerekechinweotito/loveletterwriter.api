
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from . import crud







SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24

pwd_hash=CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password):
    return pwd_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_hash.verify(plain_password, hashed_password)


def authenticate(db:Session,email:str, password:str):
    user=crud.UserCrud.get_user_by_email(db, email)
    exception= HTTPException(status_code=400, detail='invalid email or password')
    if not user:
        raise exception
    if not verify_password(password, user.password):
        raise exception
    return user

from dotenv import load_dotenv
import os 
load_dotenv()

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from . import crud
import os
import boto3
import openai
from botocore.exceptions import ClientError
from twilio.rest import Client



SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 15
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24

pwd_hash=CryptContext(schemes=['bcrypt'], deprecated='auto')

# Setup Twilio
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Setup openai
openai.api_key = os.getenv("OPENAI_API_KEY", None)

# Setup SES
FROM_EMAIL = os.getenv("FROM_EMAIL")
AWS_REGION = os.getenv("AWS_REGION")

email_client = boto3.client("ses", region_name=AWS_REGION)




def hash_password(password):
    return pwd_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_hash.verify(plain_password, hashed_password)


def authenticate(db:Session,email:str, password:str):
    user=crud.UserCrud.get_user_by_email(db, email)
    exception= HTTPException(status_code=400, detail='invalid email or password')
    if not user:
        raise exception
    if not verify_password(password, user.password):
        raise exception
    return user


def generate_letter(prompt):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    text = response["choices"][0]["text"]
    return text


def send_sms(letter):
    twilio_client.messages.create(
        body=letter.letter, from_=twilio_phone_number, to=letter.reciever.phone_number
    )


def send_email(letter):
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = letter.letter

    # The HTML body of the email.
    BODY_HTML = f"""<html>
        <head></head>
        <body>
            <h1>Love letter from {letter.sender.name}</h1>
            {letter.letter}
        </body>
        </html>
    """

    # Try to send the email.
    try:
        # Provide the contents of the email.
        response = email_client.send_email(
            Destination={
                "ToAddresses": [
                    letter.reciever.email,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": "UTF-8",
                        "Data": BODY_HTML,
                    },
                    "Text": {
                        "Charset": "UTF-8",
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": "UTF-8",
                    "Data": f"Love letter from {letter.sender.name}",
                },
            },
            Source=FROM_EMAIL,
        )
    # Display an error if something goes wrong.
    except ClientError as e:
        print(e.response["Error"]["Message"])
    return response

