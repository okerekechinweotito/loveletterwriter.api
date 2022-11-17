import os

import openai
from twilio.rest import Client

twilio_account_sid = os.environ.get("TWILIO_ACCOUNT_SID", None)
twilio_auth_token = os.environ.get("TWILIO_AUTH_TOKEN", None)
twilio_phone_number = os.environ.get("TWILIO_PHONE_NUMBER", None)
twilio_client = Client(twilio_account_sid, twilio_auth_token)
openai.api_key = os.environ.get("OPENAI_API_KEY", None)


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


def send_sms(reciever, text):
    twilio_client.messages.create(
        body=text, from_=twilio_phone_number, to=reciever.phone_number
    )
