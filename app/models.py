from sqlalchemy import Column, Integer, String, ForeignKey, Float, Index, create_engine, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

# ORDER TABLE
class CreateOrder(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(256), nullable=False)
    pickup_date = Column(String(256), nullable=False)
    sender_country = Column(Date, nullable=False)
    receiver_country = Column(String(256), nullable=False)
    sender_number = Column(String(20), nullable=False)  # Adjust size as necessary
    cargo_type = Column(String(256), nullable=False)
    pickup_location = Column(String(256), nullable=False)
    delivery_location = Column(String(256), nullable=False)
    remarks = Column(String(512), default="", nullable=True)  # Default to empty string
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship to the User table
    creator = relationship("User", back_populates="orders")

# USER TABLE
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(256), nullable=False)
    user_number = Column(String(256), unique=True, nullable=False)
    user_password = Column(String(256), nullable=False)
    
        # New fields for auto-detection
    signup_month = Column(String, nullable=False)  # e.g., 'October'
    signup_year = Column(Integer, nullable=False)   # e.g., 2024
    is_active = Column(Boolean, default=True)

    # Relationship to the Order table
    orders = relationship("CreateOrder", back_populates="creator")

# PAYMENT TABLE
class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    payment_status = Column(String(50), nullable=False, default="pending")  # Using String for payment status
    tracking_id = Column(String(256), ForeignKey('live_tracking_update.tracking_id'), unique=True, nullable=False)

    # Relationship with LiveUpdate
    live_update = relationship("LiveUpdate", back_populates="payment")

# ORDER TRACKING LIVE UPDATE
class LiveUpdate(Base):
    __tablename__ = 'live_tracking_update'

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String(256), unique=True, nullable=False)
    order_confirmed = Column(String(256), nullable=True)
    package_pickup = Column(String(256), nullable=True)
    move_to = Column(String(256), nullable=True)
    clear_custom = Column(String(256), nullable=True)
    ready_to_delivery = Column(String(256), nullable=True)
    package_delivered = Column(String(256), nullable=True)

    # One-to-one relationship with Payment
    payment = relationship("Payment", back_populates="live_update")

    # One-to-one relationship with PaymentDetails
    payment_details = relationship("PaymentDetails", back_populates="live_update")

# PAYMENT DETAILS TABLE
class PaymentDetails(Base):
    __tablename__ = 'payment_details'

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String(256), ForeignKey("live_tracking_update.tracking_id"), unique=True, nullable=False)
    payment_status = Column(String(50), default="pending")  # Using String for payment status
    payment_screenshot = Column(String(512), nullable=True)  # Store file path
    bill_copy = Column(String(512), nullable=True)  # Store file path

    # Relationship back to LiveUpdate
    live_update = relationship("LiveUpdate", back_populates="payment_details")

# Create engine for PostgreSQL
DATABASE_URL = "postgresql://Enbassy:Embassy1@localhost:5432/cargoapp"
engine = create_engine(DATABASE_URL)

# Create all tables
# Base.metadata.create_all(engine)
