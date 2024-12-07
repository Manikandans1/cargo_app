from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..respository import ordertrackingupdate, order


router = APIRouter(
    tags=['Live Tracking Update']
)
get_db = database.get_db

# ---------ORDER LIVE UPDATE DEATIL---------
@router.post('/orders/liveupdate/', status_code=status.HTTP_201_CREATED)
def LiveUpdates(orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveUpdates(orders, db)


@router.get('/orders/liveupdate/{tracking_id}', status_code=200)
def liveupdate_id(tracking_id: int, db: Session = Depends(get_db)):
    liveupdate = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == str(tracking_id)).first()
    if not liveupdate:
        raise HTTPException(status_code=404, detail="LiveUpdate not found")

    # Convert string "true"/"false" to actual bool
    liveupdate.package_pickup = liveupdate.package_pickup == 'true'
    liveupdate.clear_custom = liveupdate.clear_custom == 'true'
    liveupdate.package_delivered = liveupdate.package_delivered == 'true'
    liveupdate.order_confirmed = liveupdate.order_confirmed == 'true'
    liveupdate.ready_to_delivery = liveupdate.ready_to_delivery == 'true'

    return liveupdate


# ------TRACKING ID TO ORDER LIVE UPDATE DEATILS--------------
@router.put('/orders/liveupdate/{tracking_id}',status_code=status.HTTP_202_ACCEPTED)
def LiveTrackUpdate(tracking_id:int, orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveTrackUpdate(tracking_id,orders,db)



@router.post('/orders/{tracking_id}/details/', status_code=status.HTTP_201_CREATED)
def create_sender_receiver_details(tracking_id: str, 
                                    sender_details: schemas.Sender, 
                                    receiver_details: schemas.Receiver, 
                                    db: Session = Depends(get_db)):
    # Check if the LiveUpdate with the provided tracking_id exists
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == tracking_id).first()
    
    if not live_update:
        raise HTTPException(status_code=404, detail="LiveUpdate not found")

    # Create sender details
    sender = models.Sender(**sender_details.dict(), live_update_id=live_update.id)
    db.add(sender)

    # Create receiver details
    receiver = models.Receiver(**receiver_details.dict(), live_update_id=live_update.id)
    db.add(receiver)

    db.commit()
    db.refresh(sender)
    db.refresh(receiver)

    return {
        "tracking_id": tracking_id,
        "sender": sender,
        "receiver": receiver
    }


# Retrieve sender and receiver details
@router.get('/orders/{tracking_id}/details/', status_code=status.HTTP_200_OK)
def get_sender_receiver_details(tracking_id: str, db: Session = Depends(get_db)):
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == tracking_id).first()
    
    if not live_update:
        raise HTTPException(status_code=404, detail="LiveUpdate not found")

    sender = db.query(models.Sender).filter(models.Sender.live_update_id == live_update.id).first()
    receiver = db.query(models.Receiver).filter(models.Receiver.live_update_id == live_update.id).first()

    return {
        "tracking_id": tracking_id,
        "sender": sender,
        "receiver": receiver
    }