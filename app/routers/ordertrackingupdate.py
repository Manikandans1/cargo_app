from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..respository import ordertrackingupdate, order


router = APIRouter(
    tags=['Live Tracking Update']
)
get_db = database.get_db



# # Route to create an order and automatically verify OTP
# @router.post('/orders/', status_code=status.HTTP_201_CREATED)
# def create_order(orders: schemas.Create_Order, db: Session = Depends(get_db)):
#     return order.create_orders(orders, db)

# ---------ORDER LIVE UPDATE DEATIL---------
@router.post('/orders/liveupdate/', status_code=status.HTTP_201_CREATED)
def LiveUpdates(orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveUpdates(orders, db)


# ------TRACKING ID TO GET ORDER LIVE UPDATE DEATILS--------------
@router.get('/orders/liveupdate/{tracking_id}',status_code=200)
def liveupdate_id(tracking_id:int, db: Session = Depends(get_db)):
    return ordertrackingupdate.liveupdate_id(tracking_id,db)

# ------TRACKING ID TO ORDER LIVE UPDATE DEATILS--------------
@router.put('/orders/liveupdate/{tracking_id}',status_code=status.HTTP_202_ACCEPTED)
def LiveTrackUpdate(tracking_id:int, orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveTrackUpdate(tracking_id,orders,db)