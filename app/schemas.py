from pydantic import BaseModel, Field
from typing import List, Optional

#ORDER
class Create_Order(BaseModel):
    customer_name: str
    pickup_date: str
    sender_country: str
    receiver_country: str
    sender_number: str
    cargo_type: str
    pickup_location: str
    delivery_location: str
    remarks: str | None = None


    class Config():
        orm_mode = True
   # description: str | None = None
   # price: float
   # tax: float | None = None



#CREATE THE NEW USER
class User(BaseModel):
    user_name: str
    #user_number: str
    user_number: str
    user_password: str


# USER GET PAYMENT DEATILS---COMPANY WILL CREATE DEATILS
class Payment(BaseModel):
    tracking_id: str
    payment_status: str = "paid"
    payment_screenshot: Optional[str]

class PaymentResponse(BaseModel):
    detail: str




# -------ORDER TRACKING LIVE UPDATE-------------
class LiveUpdate(BaseModel):
    tracking_id: str = Field(..., allow_mutation=False)
    order_confirmed: str
    package_pickup: str | None = None
    move_to: str | None = None
    clear_custom: str | None = None
    ready_to_delivery: str | None = None
    package_delivered: str | None = None
    class Config():
        # Make the model immutable
        allow_mutation = True

    def __setattr__(self, name, value):
        if name == "tracking_id" and hasattr(self, "tracking_id"):
            raise ValueError("The tracking_id cannot be updated once it is set.")
        super().__setattr__(name, value)


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
    orders: List[Create_Order] = []
    class Config():
        orm_mode = True



#----WHAT EVER WE WANT TO SHOW THE USER DEFINE THE NAME----
class Show_Create_Order(BaseModel):
    customer_name: str
    pickup_location: str
    creator: Show_user


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