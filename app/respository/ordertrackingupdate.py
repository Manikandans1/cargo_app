from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def LiveUpdates(orders: schemas.LiveUpdate, db: Session):
    # Check if the tracking_id already exists in the database
    existing_tracking_id = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == orders.tracking_id).first()
    
    # If tracking_id exists, raise an HTTP 400 Bad Request error
    if existing_tracking_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tracking ID {orders.tracking_id} already exists. Please use a unique tracking ID."
        )
    
    # Create a new LiveUpdate record if tracking_id is unique
    live_update_details = models.LiveUpdate(
        tracking_id=orders.tracking_id,
        order_confirmed=orders.order_confirmed,
        package_pickup=orders.package_pickup,
        move_to=orders.move_to,
        clear_custom=orders.clear_custom,
        ready_to_delivery=orders.ready_to_delivery,
        package_delivered=orders.package_delivered 
    )
    
    db.add(live_update_details)
    db.commit()
    db.refresh(live_update_details)
    
    return live_update_details


def liveupdate_id(tracking_id:int,db:Session):
    liveupdate_id = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == str(tracking_id)).first()
    if not liveupdate_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"In this liveupdate id = {id} is not available")
    return liveupdate_id


def LiveTrackUpdate(tracking_id:int,orders: schemas.LiveUpdate, db:Session):
    live_update =  db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == str(tracking_id)).first()
    if not live_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"The order liveUpdate id = {tracking_id} is not available")
    #live_update.LiveTrackUpdate(orders.dict())
    update_data = orders.dict(exclude={'tracking_id'})

    for key, value in update_data.items():
        setattr(live_update, key, value)
    db.commit()
    db.refresh(live_update)
    return 'updated sucessfully'