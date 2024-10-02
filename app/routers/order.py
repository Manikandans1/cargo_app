from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, database, models, oauth2
from typing import List
from sqlalchemy.orm import Session
from ..respository import order


router = APIRouter(
    tags=['Orders']
)
get_db = database.get_db



@router.get('/orders/', response_model=List[schemas.Show_Create_Order])
def view_all_orders(db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.get_all(db)


#NEW ORDER CREATE
@router.post('/orders/', status_code=status.HTTP_201_CREATED)
def create_orders(orders: schemas.Create_Order, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.create_orders(orders, db)
 
# Route to verify the OTP
@router.post('/orders/verify_otp/', status_code=status.HTTP_200_OK)
def verify_otp(otp_data: schemas.OTPVerification):
    return order.verify_otp(otp_data.order_id, otp_data.otp)

#DELETE
@router.delete('/orders/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.destroy(id,db)


#UPDATE
@router.put('/orders/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id:int, orders: schemas.Create_Order, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.update(id,orders,db)




#ORDER UNIQUE ID TO GET DEATILS
@router.get('/orders/{id}',status_code=200,response_model=schemas.Show_Create_Order)
def track_id(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return order.track_id(id,db)

