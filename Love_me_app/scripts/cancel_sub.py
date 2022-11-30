import time
from datetime import datetime
from ..dependencies import get_current_user
from fastapi import HTTPException,Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..import models
import threading





"""this thread checks for the current user's subscription end date and disables accordingly"""


def Cancel_sub(db: Session = Depends(get_db),user:dict = Depends(get_current_user)):

    get_date = user.sub_end_date
    date_in_seconds = get_date.timestamp()
    while date_in_seconds:
        print("time till amagedon",date_in_seconds, end='\r')
        time.sleep(1)
        date_in_seconds -= 1
    user.is_sub_active = False
    user.sub_end_date = datetime.now()
    db.commit()

t1 = threading.Thread(target=Cancel_sub, name="cancel_sub")
t1.start()

