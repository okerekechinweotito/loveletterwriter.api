#Import libraries
import os
from fastapi import BackgroundTasks

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig



async def password_reset(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html',
    )
    pass
