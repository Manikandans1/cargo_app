from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

#ORDER TABLE
class Create_Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer,primary_key=True, index=True)
    coustmer_name =  Column(String)
    pickup_date = Column(String)
    sender_country= Column(String)
    receiver_country = Column(String)
    sender_number = Column(String)
    cargo_type = Column(String)
    pickup_location = Column(String)
    delivery_location = Column(String)
    remarks = Column(String)
    user_id = Column(Integer,ForeignKey('users.id'))

    creator = relationship("User",back_populates="orders")



#USER TABLE
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True) 
    user_name = Column(String)
    #user_number = Column(String)
    user_email = Column(String)
    user_password = Column(String)

    orders = relationship("Create_Order",back_populates="creator")



# ---------USER GET PAYMENT DEATILS-----COMPANY WILL CREATE DEATILS---
class Payment(Base):

    __tablename__ = 'payment'

    id = Column(Integer,primary_key=True, index=True) 
    amount = Column(String)
    payment_status = Column(String)
    tracking_id = Column(String)


# -------ORDER TRACKING LIVE UPDATE-------------
class LiveUpdate(Base):

    __tablename__ = 'LiveTrackingUpdate'

    id = Column(Integer,primary_key=True, index=True) 

    tracking_id = Column(String,unique=True, nullable=False)
    order_confirmed = Column(String)
    package_pickup = Column(String)
    move_to = Column(String)
    clear_custom = Column(String)
    ready_to_delivery = Column(String)
    package_delivered = Column(String)

    payment_details = relationship("PaymentDetails", uselist=False, back_populates="live_update")



class PaymentDetails(Base):
    __tablename__ = 'payment_details'
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, ForeignKey("LiveTrackingUpdate.tracking_id"), unique=True, nullable=False)
    payment_status = Column(String, default="pending")
    payment_screenshot = Column(String)  # Store file path or use BYTEA for binary
    bill_copy = Column(String, nullable=True) 
    
    live_update = relationship("LiveUpdate", back_populates="payment_details")