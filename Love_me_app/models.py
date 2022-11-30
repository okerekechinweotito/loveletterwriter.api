from sqlalchemy import Column, Integer, String, Time, TEXT, DateTime, Boolean, ForeignKey, Float, LargeBinary
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    image = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    facebook_id = Column(String(255))
    google_id = Column(String(255))
    is_sub_active = Column(Boolean, default=False)
    sub_end_date = Column(DateTime)
    plan_type = Column(String(255))
    is_reminder = Column(Boolean, default=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    free_trial = Column(Boolean,default=True)
    receiver = relationship('Receiver', back_populates='sender')
    letter = relationship('Letter', back_populates='writer')
    schedule = relationship('Schedule', back_populates='user')
    ai_trainer_value = relationship('AiTrainerValue', back_populates='user')
    transaction = relationship('Transaction', back_populates='user')
    reset_pass = relationship('ResetPass', back_populates='user')
    product_review = relationship('ProductReview', back_populates='user')
    #is_admin = Boolean(default=False)


class Receiver(Base):
    __tablename__ = "receivers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    phone_number = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    sender = relationship('User', back_populates='receiver')
    letter = relationship('Letter', back_populates='receiver')
    ai_trainer_value = relationship('AiTrainerValue', back_populates='receiver')


class Letter(Base):
    __tablename__ = "letters"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'), nullable=True)
    title = Column(TEXT)
    letter = Column(TEXT)
    date_sent = Column(DateTime(timezone=True), nullable=True)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    writer = relationship('User', back_populates='letter')
    receiver = relationship('Receiver', back_populates='letter')
    schedule= relationship('Schedule',back_populates='letter')


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'))
    letter_id=Column(Integer,ForeignKey('letters.id'))
    schedule_time = Column(DateTime(timezone=True))
    completed=Column(Boolean, default=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='schedule')
    letter=relationship('Letter', back_populates='schedule')


class AiTrainer(Base):
    __tablename__ = "ai_trainers"
    id = Column(Integer, primary_key=True, index=True)
    ui_name = Column(String(255))
    ai_word = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    ai_trainer_value = relationship('AiTrainerValue', back_populates='ai_trainer')


class AiTrainerValue(Base):
    __tablename__ = "ai_trainer_values"
    id = Column(Integer, primary_key=True, index=True)
    ai_trainer_id = Column(Integer, ForeignKey('ai_trainers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    receiver_id = Column(Integer, ForeignKey('receivers.id'))
    value = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    ai_trainer = relationship('AiTrainer', back_populates='ai_trainer_value')
    user = relationship('User', back_populates='ai_trainer_value')
    receiver = relationship('Receiver', back_populates='ai_trainer_value')


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(255))
    months = Column(Integer)
    amount = Column(Float)
    date_created = Column(DateTime)
    amount = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    transaction = relationship('Transaction', back_populates='subscription')

    def __repr__(self):
        return f'{self.name} {self.amount}'


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subscription_id = Column(Integer, ForeignKey('subscriptions.id'))
    ref_no = Column(String(255))
    date_created = Column(String(255))
    user = relationship('User',back_populates='transaction')
    subscription = relationship('Subscription',back_populates='transaction')

    
    

class ResetPass(Base):
    __tablename__ = "reset_pass"
    id = Column(Integer, primary_key=True, index=True)
    pin = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))
    is_used = Column(Boolean)
    expiry_date = Column(DateTime)
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='reset_pass')


class BlackListedTokens(Base):
    __tablename__ = "black_listed_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255))
    expiry_date = Column(String(255))
    blacklisted_on = Column(DateTime(timezone=True), server_default=func.now())

class ProductReview(Base):
    __tablename__ = "product_reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    review = Column(String(255))
    date_created = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship('User', back_populates='product_review')
 
class RoleApplication(Base):
    __tablename__ = "role_application"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    linked_in = Column(String(255))
    cover_letter = Column(LargeBinary)
    cv = Column(LargeBinary)
    
class MailSubscriber(Base):
    __tablename__ = "mail_subscribers"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255))
    

