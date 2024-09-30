from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status

def get_all(db : Session):
    view_all_order = db.query(models.CreateOrder).all()
    return view_all_order

def create_orders(orders: schemas.Create_Order,db: Session):
    new_orders = models.CreateOrder(
        customer_name = orders.customer_name, 
        pickup_location = orders.pickup_location, 
        delivery_location = orders.delivery_location, 
        remarks = orders.remarks,
        pickup_date = orders.pickup_date,
        sender_country = orders.sender_country,
        receiver_country = orders.receiver_country,
        sender_number = orders.sender_number,
        cargo_type = orders.cargo_type,
        user_id= 1
        )
    db.add(new_orders)
    db.commit()
    db.refresh(new_orders)
    return new_orders

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