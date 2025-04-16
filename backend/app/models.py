from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, index=True, nullable=True)

    tickets = relationship('Ticket', back_populates='owner')

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    ticket_code = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    payment_id = Column(Integer, ForeignKey('payments.id'))  # Add this field to link the ticket to a payment

    owner = relationship('User', back_populates='tickets')
    payment = relationship('Payment', back_populates='tickets')  # Change the relationship here to one-to-many

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, default=5000)
    reference = Column(String, unique=False, nullable=False)

    tickets = relationship('Ticket', back_populates='payment')  # Change here to allow multiple tickets

class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)