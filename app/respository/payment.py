from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status




def Payments(orders: schemas.Payment, db: Session):
    # Check if the tracking_id exists
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == orders.tracking_id).first()
    if not live_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tracking ID {orders.tracking_id} not found."
        )

    # Check if payment details already exist, if so, update them
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == orders.tracking_id).first()

    if not payment_detail:
        payment_detail = models.PaymentDetails(
            tracking_id=orders.tracking_id,
            payment_status=orders.payment_status,
            payment_screenshot=orders.payment_screenshot
        )
        db.add(payment_detail)
    else:
        payment_detail.payment_status = orders.payment_status
        payment_detail.payment_screenshot = orders.payment_screenshot

    db.commit()
    return {"detail": "Payment updated successfully"}

def payment_id(tracking_id: str, db: Session):
    # Retrieve all details associated with a tracking ID
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == tracking_id).first()
    if not live_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tracking ID {tracking_id} not found."
        )
    
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()
    
    # Return the live update and payment details
    return {
        "tracking_id": live_update.tracking_id,
        "order_details": {
            "order_confirmed": live_update.order_confirmed,
            "package_pickup": live_update.package_pickup,
            # Add other fields...
        },
        "payment_details": {
            "payment_status": payment_detail.payment_status if payment_detail else "Not paid",
            "payment_screenshot": payment_detail.payment_screenshot if payment_detail else None
        }
    }