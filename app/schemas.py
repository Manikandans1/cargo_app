from pydantic import BaseModel, Field, constr
from typing import List, Optional
from datetime import date

#ORDER
class Create_Order(BaseModel):
    customer_name: str
    pickup_date: str
    sender_country: str
    receiver_country: str
    sender_number: str
    cargo_type: str
    pickup_location: str
    # delivery_location: str
    remarks: str | None = None
    
    class Config():
        orm_mode = True
   # description: str | None = None
   # price: float
   # tax: float | None = None

# Schema for OTP verification
class OTPVerification(BaseModel):
    order_id: int
    otp: str


#CREATE THE NEW USER
class User(BaseModel):
    user_name: str
    user_number: str  # Enforce non-empty user_number
    user_password: str

class ShowUser(BaseModel):
    # id: int
    user_name: str
    user_number: str
    signup_month: str
    signup_year: int
    # is_active: bool

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    user_name: Optional[str]
    user_number: Optional[str]

# USER GET PAYMENT DEATILS---COMPANY WILL CREATE DEATILS
class Payment(BaseModel):
    tracking_id: str
    payment_status: str = "paid"
    payment_screenshot: Optional[str]

class PaymentResponse(BaseModel):
    detail: str


# -------ORDER TRACKING LIVE UPDATE-------------


class LiveUpdate(BaseModel):
    tracking_id: str
    order_confirmed: Optional[bool] = True
    package_pickup: Optional[bool] = False
    move_to: Optional[str] = "No"
    clear_custom: Optional[bool] = False
    ready_to_delivery: Optional[bool] = False
    package_delivered: Optional[bool] = False

    class Config:
        orm_mode = True 


class Sender(BaseModel):
    name: str
    country: str
    shipping_type: str
    weight_cbm: str
    quantity: str
    order_date: str
    expected_delivery_day: str
    pickup_driver: str
    delivery_driver: str
    service_charge: str

class Receiver(BaseModel):
    name: str
    country: str
    district: str
    city: str



class PaymentUpdate(BaseModel):
    tracking_id: str
    payment_status: str = "paid"

class PaymentResponse(BaseModel):
    detail: str
    bill_location: Optional[str] = None


class Show_user(BaseModel):
    user_name: str
    #user_number: str
    user_number: str
    # orders: List[Create_Order] = []
    class Config():
        orm_mode = True



#----WHAT EVER WE WANT TO SHOW THE USER DEFINE THE NAME----
class Show_Create_Order(BaseModel):
    customer_name: str
    pickup_location: str
    # creator: Show_user


    class Config():
        orm_mode = True



class Login(BaseModel):
    username: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_number: str | None = None