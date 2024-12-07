from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File, Form
from .. import schemas, database, models, oauth2
from typing import List, Union
from sqlalchemy.orm import Session
from ..respository import payment
import shutil
import os
from fastapi.responses import FileResponse
import stripe
from pydantic import BaseModel


router = APIRouter(
    tags=['Payments Bill']
)
get_db = database.get_db

# ---------------------------------------------------------------------------------------
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import stripe

# Initialize the FastAPI app
# app = FastAPI()

# Set your Stripe secret key here
stripe.api_key = "sk_test_51QMRv3Fj439McXMca9tS2CfJlcUqH5OkoHa9sZQl9DW4bIkYn6vxVuinkQU4vQnUzXq87H2ipaEfOdh0HNJXXKRw0082y7oiW6"  # Ensure you set the secret key in the environment

# Set up PostgreSQL connection
DATABASE_URL = "postgresql://Embassy:Embassy12@localhost:5432/cargoapp"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class PaymentIntentRequest(BaseModel):
    amount: float  # Total amount to be charged in cents (for example, $10 = 1000 cents)
    currency: str  # Currency to charge in (e.g., 'usd')

class PaymentIntentResponse(BaseModel):
    client_secret: str
    amount: float

class RefundRequest(BaseModel):
    payment_intent_id: str  # The ID of the payment intent
    amount: float  # Refund amount (in cents)

class RefundResponse(BaseModel):
    status: str
    refund_id: str
    refunded_amount: float

class ChargesRequest(BaseModel):
    order_id: str  # Unique order ID
    box_charges: float  # Charges for the box
    freight_charges: float  # Charges for freight

class ChargesResponse(BaseModel):
    order_id: str
    box_charges: float
    freight_charges: float
    total_charges: float

# Define the Charges table using SQLAlchemy
class Charges(Base):
    __tablename__ = "charges"

    order_id = Column(String, primary_key=True, index=True)
    box_charges = Column(Float)
    freight_charges = Column(Float)
    total_charges = Column(Float)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PaymentRequest(BaseModel):
    amount: int  # Amount in cents

@router.post("/create-payment-intent")
async def create_payment_intent(data: PaymentRequest):
    try:
        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=data.amount,
            currency="usd",  # Replace with your desired currency
            payment_method_types=["card"],
        )
        return {"client_secret": intent.client_secret}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




# Endpoint to confirm the payment on the backend (after frontend completes user interaction)
@router.post("/confirm-payment/")
async def confirm_payment(payment_intent_id: str):
    try:
        payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
        if payment_intent.status == "succeeded":
            return {"status": "success", "payment_intent_id": payment_intent.id}
        else:
            raise HTTPException(status_code=400, detail="Payment failed.")

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")


# Endpoint to refund a payment (e.g., after cancellation)
@router.post("/refund-payment/", response_model=RefundResponse)
async def refund_payment(refund_request: RefundRequest):
    try:
        refund = stripe.Refund.create(
            payment_intent=refund_request.payment_intent_id,
            amount=int(refund_request.amount * 100),  # Refund amount in cents
        )

        return RefundResponse(
            status="Success",
            refund_id=refund.id,
            refunded_amount=refund.amount / 100,  # Convert back to dollars
        )

    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=f"Stripe error: {str(e)}")


# Endpoint to enter box and freight charges for an order
@router.post("/enter-charges/", response_model=ChargesResponse)
async def enter_charges(charges_request: ChargesRequest, db: Session = Depends(get_db)):
    """
    This endpoint allows the company to enter box and freight charges for an order.
    The charges will be stored in the database and returned with the total charge.
    """
    try:
        total_charges = charges_request.box_charges + charges_request.freight_charges

        # Store the charges in the database
        charge = Charges(
            order_id=charges_request.order_id,
            box_charges=charges_request.box_charges,
            freight_charges=charges_request.freight_charges,
            total_charges=total_charges,
        )
        db.add(charge)
        db.commit()

        return ChargesResponse(
            order_id=charges_request.order_id,
            box_charges=charges_request.box_charges,
            freight_charges=charges_request.freight_charges,
            total_charges=total_charges,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error entering charges: {str(e)}")


# Endpoint to get charges for an order (GET request)
@router.get("/get-charges/{order_id}", response_model=ChargesResponse)
async def get_charges(order_id: str, db: Session = Depends(get_db)):
    """
    This endpoint retrieves the charges for a given order from the database.
    """
    try:
        charge = db.query(Charges).filter(Charges.order_id == order_id).first()

        if not charge:
            raise HTTPException(status_code=404, detail="Order not found")

        return ChargesResponse(
            order_id=charge.order_id,
            box_charges=charge.box_charges,
            freight_charges=charge.freight_charges,
            total_charges=charge.total_charges,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching charges: {str(e)}")

