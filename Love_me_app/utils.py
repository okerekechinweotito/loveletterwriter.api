import os

import boto3
import openai
from botocore.exceptions import ClientError
from twilio.rest import Client

# Setup Twilio
twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", None)
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", None)
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER", None)
twilio_client = Client(twilio_account_sid, twilio_auth_token)

# Setup openai
openai.api_key = os.environ.get("OPENAI_API_KEY", None)

# Setup SES
FROM_EMAIL = os.environ.get("FROM_EMAIL", None)
AWS_REGION = os.environ.get("AWS_REGION", None)
email_client = boto3.client("ses", region_name=AWS_REGION)


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
