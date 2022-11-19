from .utils import hash_password
from .import models, schemas
import uuid


class UserCrud:
    

    def get_user_by_id(db,id:str):
        return db.query(models.User).filter(models.User.id==id).first()

    def get_user_by_email(db,email:str):
        return db.query(models.User).filter(models.User.email==email).first()



    def create_user(db,user:schemas.UserCreate):
        password=hash_password(user.password)
        db_user=models.User(email=user.email, password=password, first_name=user.first_name, last_name=user.last_name )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user





