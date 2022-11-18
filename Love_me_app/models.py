from sqlalchemy import Column,Integer,String,Time,Date,DateTime,Boolean,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    email = Column(String)
    facebook_id = Column(String)
    google_id = Column(String)
    is_sub_active = Column(Boolean, default=False)
    sub_end_date = Column(DateTime)
    is_reminder = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    receiver = relationship('Receiver',back_populates='sender')
    letter = relationship('Letter',back_populates='writer')
    schedule = relationship('Schedule',back_populates='user')
    ai_trainer_value = relationship('AiTrainerValue',back_populates='user')
    transaction = relationship('Transaction',back_populates='user')
    reset_pass = relationship('ResetPass',back_populates='user')

class Receiver(Base):
    __tablename__ = "receivers"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))
    date_created = Column(DateTime)
    sender = relationship('User',back_populates='receiver')
    letter = relationship('Letter',back_populates='receiver')
    schedule = relationship('Schedule',back_populates='receiver')
    ai_trainer_value = relationship('AiTrainerValue',back_populates='receiver')
    

class Letter(Base):
    __tablename__ = "letters"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    receiver_id = Column(Integer,ForeignKey('receivers.id'))
    letter = Column(String)
    date_created = Column(DateTime)
    writer = relationship('User',back_populates='letter')
    receiver = relationship('Receiver',back_populates='letter')

class Schedule(Base):
    __tablename__="schedules"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    receiver_id = Column(Integer,ForeignKey('receivers.id'))
    schedule_time = Column(Time)
    date_created = Column(DateTime)
    user = relationship('User',back_populates='schedule')
    receiver = relationship('Receiver',back_populates='schedule')

class AiTrainer(Base):
    __tablename__="ai_trainers"
    id = Column(Integer,primary_key=True,index=True)
    ui_name = Column(String)
    ai_word = Column(String)
    date_created = Column(DateTime)
    ai_trainer_value = relationship('AiTrainerValue',back_populates='ai_trainer')

class AiTrainerValue(Base):
    __tablename__="ai_trainer_values"
    id = Column(Integer,primary_key=True,index=True)
    ai_trainer_id = Column(Integer,ForeignKey('ai_trainers.id'))
    user_id = Column(Integer,ForeignKey('users.id'))
    receiver_id = Column(Integer,ForeignKey('receivers.id'))
    value = Column(String)
    date_created = Column(DateTime)
    ai_trainer = relationship('AiTrainer',back_populates='ai_trainer_value')
    user = relationship('User',back_populates='ai_trainer_value')
    receiver = relationship('Receiver',back_populates='ai_trainer_value')


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    description = Column(String)
    months = Column(Integer)
    total_sms = Column(Integer)
    amount = Column(String)
    date_created = Column(DateTime)
    transaction = relationship('Transaction',back_populates='subscription')


class Transaction(Base):
    __tablename__="transactions"
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    subscription_id = Column(Integer,ForeignKey('subscriptions.id'))
    ref_no = Column(String)
    date_created = Column(DateTime)
    user = relationship('User',back_populates='transaction')
    subscription = relationship('Subscription',back_populates='transaction')

class ResetPass(Base):
    __tablename__="reset_pass"
    id = Column(Integer,primary_key=True,index=True)
    pin = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))
    is_used = Column(Boolean)
    expiry_date = Column(DateTime)
    date_created = Column(DateTime)
    user = relationship('User',back_populates='reset_pass')

class BlackListedTokens(Base):
    __tablename__="black_listed_tokens"
    id = Column(Integer,primary_key=True,index=True)
    token = Column(String)
    expiry_date = Column(String)
    blacklisted_on = Column(DateTime)
