from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..respository import ordertrackingupdate


router = APIRouter(
    tags=['Live Tracking Update']
)
get_db = database.get_db


# ---------ORDER LIVE UPDATE DEATIL---------
@router.post('/orders/liveupdate/', status_code=status.HTTP_201_CREATED)
def LiveUpdates(orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveUpdates(orders, db)


# ------TRACKING ID TO GET LIVE UPDATE DEATILS--------------
@router.get('/orders/liveupdate/{tracking_id}',status_code=200)
def liveupdate_id(tracking_id:int, db: Session = Depends(get_db)):
    return ordertrackingupdate.liveupdate_id(tracking_id,db)

# ------TRACKING ID TO LIVE UPDATE DEATILS--------------
@router.put('/orders/liveupdate/{tracking_id}',status_code=status.HTTP_202_ACCEPTED)
def LiveTrackUpdate(tracking_id:int, orders: schemas.LiveUpdate, db: Session = Depends(get_db)):
    return ordertrackingupdate.LiveTrackUpdate(tracking_id,orders,db)