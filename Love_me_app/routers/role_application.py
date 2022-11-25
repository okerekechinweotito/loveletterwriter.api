from fastapi import FastAPI, Form, UploadFile
from typing import Union
from sqlalchemy.orm import Session
from ..database import get_db

from .. import models, schemas

db = get_db()
app = FastAPI()


@app.get("/role-application/")
async def role_application(db: Session,
    full_name: str = Form(),
    email: str = Form(),
    linkedin: str = Form(),
    cover_letter: Union[UploadFile, None] = None,
    cv: Union[UploadFile, None] = None
    ):

    if not cover_letter:
        return {"message": "Cover letter not uploaded"}
    if not cv:
        return {"message": "CV not uploaded"}
    db_application = models.RoleApplication(
        full_name=full_name,
        email=email,
        linked_in= linkedin)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return {"message": "Application successful!"}

