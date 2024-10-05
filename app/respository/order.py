from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
import random


# In-memory storage for OTPs (order_id: OTP)
otp_storage = {}

def generate_otp():
    """Generates a random 4-digit OTP."""
    return str(random.randint(1000, 9999))

def create_orders(orders: schemas.Create_Order, db: Session):
    """Creates a new order and generates an OTP."""
    otp = generate_otp()  # Generate OTP
    new_order = models.CreateOrder(
        customer_name=orders.customer_name, 
        pickup_location=orders.pickup_location, 
        delivery_location=orders.delivery_location, 
        remarks=orders.remarks,
        pickup_date=orders.pickup_date,
        sender_country=orders.sender_country,
        receiver_country=orders.receiver_country,
        sender_number=orders.sender_number,
        cargo_type=orders.cargo_type,
        user_id=1
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Store the OTP in the in-memory storage for verification
    otp_storage[new_order.id] = otp

    # Simulate sending OTP (in real-world, you might print it or log it for testing)
    print(f"OTP for Order {new_order.id} is {otp}. Sent to {orders.sender_number}")

    return {"message": "OTP generated and sent to sender's phone number", "order_id": new_order.id}

def verify_otp(order_id: int, otp: str):
    """Verifies the OTP provided by the user."""
    if order_id not in otp_storage:
        raise HTTPException(status_code=404, detail="Order not found or OTP expired")

    if otp_storage[order_id] != otp:
        raise HTTPException(status_code=400, detail="Incorrect OTP")

    # OTP is correct, remove it from the storage after successful verification
    del otp_storage[order_id]

    return {"message": "OTP verified successfully. Order confirmed."}

def get_all(db : Session):
    view_all_order = db.query(models.CreateOrder).all()
    return view_all_order


def destroy(id:int,db: Session):
    destroyy = db.query(models.CreateOrder).filter(models.CreateOrder.id == id)
    if not destroyy.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The order with id = {id} is not available")

    destroyy.delete(synchronize_session=False)
    db.commit()
    return 'order deleted'


def update(id:int,orders: schemas.Create_Order, db:Session):
    new_update = db.query(models.CreateOrder).filter(models.CreateOrder.id == id)
    if not new_update.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The order with id = {id} is not available")
    new_update.update(orders.dict())
    db.commit()
    return 'updated sucessfully'

def track_id(id:int,db:Session):
    track_id = db.query(models.CreateOrder).filter(models.CreateOrder.id == id).first()
    if not track_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"In this order id = {id} is not available")
    return track_id












# from pyfcm import FCMNotification
# import random

# # Your Firebase Cloud Messaging server key
# FCM_SERVER_KEY = 'your_fcm_server_key_here'

# # Initialize FCMNotification with the server key
# push_service = FCMNotification(api_key=FCM_SERVER_KEY)

# # In-memory storage for OTPs (order_id: OTP)
# otp_storage = {}

# def generate_otp():
#     """Generates a random 4-digit OTP."""
#     return str(random.randint(1000, 9999))

# def create_order(orders: schemas.CreateOrder, db: Session):
#     """Creates a new order and sends an OTP via FCM push notification."""
#     otp = generate_otp()  # Generate OTP

#     # Create the new order in the database
#     new_order = models.CreateOrder(
#         customer_name=orders.customer_name, 
#         pickup_location=orders.pickup_location, 
#         delivery_location=orders.delivery_location, 
#         remarks=orders.remarks,
#         pickup_date=orders.pickup_date,
#         sender_country=orders.sender_country,
#         receiver_country=orders.receiver_country,
#         sender_number=orders.sender_number,
#         cargo_type=orders.cargo_type,
#         user_id=1
#     )
#     db.add(new_order)
#     db.commit()
#     db.refresh(new_order)

#     # Store the OTP in memory for verification
#     otp_storage[new_order.id] = otp

#     # Prepare the data to send via FCM push notification
#     data_message = {
#         "title": "OTP Verification",
#         "body": f"Your OTP for Order {new_order.id} is {otp}",
#     }

#     # Send push notification to the customer's device
#     result = push_service.notify_single_device(
#         registration_id=orders.fcm_token,  # FCM token of the customer
#         message_title="OTP Verification",
#         message_body=f"Your OTP for Order {new_order.id} is {otp}",
#         data_message=data_message
#     )

#     print(f"Push notification sent: {result}")

#     return {"message": "OTP generated and sent via push notification", "order_id": new_order.id}

# def verify_otp(order_id: int, otp: str):
#     """Verifies the OTP provided by the user."""
#     if order_id not in otp_storage:
#         raise HTTPException(status_code=404, detail="Order not found or OTP expired")

#     if otp_storage[order_id] != otp:
#         raise HTTPException(status_code=400, detail="Incorrect OTP")

#     # OTP is correct, remove it from the storage after successful verification
#     del otp_storage[order_id]

#     return {"message": "OTP verified successfully. Order confirmed."}
