from fastapi import APIRouter, Depends, status, HTTPException, Response, UploadFile, File, Form
from .. import schemas, database, models, oauth2
from typing import List, Union
from sqlalchemy.orm import Session
from ..respository import payment
import shutil
import os
from fastapi.responses import FileResponse


router = APIRouter(
    tags=['Payments Bill']
)
get_db = database.get_db


# # Create or Update Payment Details
# @router.post('/orders/payment/', status_code=status.HTTP_201_CREATED)
# def Payments(orders: schemas.Payment, db: Session = Depends(get_db)):
#     return payment.Payments(orders, db)

# Get all payment and order details by tracking ID
@router.get('/orders/payment/{tracking_id}', status_code=200)
def payment_id(tracking_id: str, db: Session = Depends(get_db)):
    return payment.payment_id(tracking_id, db)





UPLOAD_DIRECTORY = "payment_screenshots"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@router.post("/orders/payment_update", response_model=schemas.PaymentResponse)
async def payment_update(
    tracking_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Fetch the LiveUpdate record by tracking_id
    live_update = db.query(models.LiveUpdate).filter(models.LiveUpdate.tracking_id == tracking_id).first()
    if not live_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with tracking_id {tracking_id} not found."
        )

    # Save the uploaded file
    file_location = f"{UPLOAD_DIRECTORY}/{tracking_id}_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update or create payment details
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()
    
    if not payment_detail:
        payment_detail = models.PaymentDetails(
            tracking_id=tracking_id,
            payment_status="under verification",
            payment_screenshot=file_location
        )
        db.add(payment_detail)
    else:
        payment_detail.payment_status = "under verification"
        payment_detail.payment_screenshot = file_location

    db.commit()

    return  {"detail": "Payment uploaded and under verification", "file_location": file_location}



@router.get("/orders/view_payment_screenshot/{tracking_id}")
async def view_payment_screenshot(tracking_id: str, db: Session = Depends(get_db)):
    # Retrieve the payment detail from the database
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()

    if not payment_detail or not payment_detail.payment_screenshot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment screenshot not found")

    file_path = payment_detail.payment_screenshot

    # Check if the file exists on disk
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Screenshot file not found")

    # Serve the file
    return FileResponse(file_path, media_type="image/jpeg", filename=f"{tracking_id}_receipt.jpg")





# Directory to store the uploaded bills
BILL_DIRECTORY = "bill_copies"

if not os.path.exists(BILL_DIRECTORY):
    os.makedirs(BILL_DIRECTORY)





@router.put("/orders/verify_payment/{tracking_id}", response_model=schemas.PaymentResponse)
async def verify_payment(
    tracking_id: str, 
    bill_file: UploadFile = File(None),  # Bill file upload (optional)
    db: Session = Depends(get_db)
):
    # Fetch the payment details by tracking_id
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()
    
    if not payment_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found")
    
    if payment_detail.payment_status != "under verification":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment is not under verification")

    # Update the payment status to "paid successfully" or continue verification
    payment_detail.payment_status = "paid successfully" if bill_file else "under verification"

    # Save the bill file if provided
    bill_location = None
    if bill_file:
        bill_location = f"{BILL_DIRECTORY}/{tracking_id}_{bill_file.filename}"
        with open(bill_location, "wb") as buffer:
            shutil.copyfileobj(bill_file.file, buffer)

        # Associate the bill with the payment details
        payment_detail.bill_copy = bill_location

    db.commit()

    return {"detail": "Payment verified and bill uploaded successfully" if bill_file else "Payment uploaded and under verification", "bill_location": bill_location}





# ----------Get Bill Copy----------
# @router.get("/orders/get_bill/{tracking_id}")
# async def get_bill(tracking_id: str, db: Session = Depends(get_db)):
#     # Fetch the payment details by tracking_id
#     payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()

#     if not payment_detail or not payment_detail.bill_copy:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill copy not found")

#     # Return the path of the bill copy (you can also serve the actual file if needed)
#     return {"bill_copy_path": payment_detail.bill_copy}




@router.get("/orders/download_bill/{tracking_id}")
async def download_bill(tracking_id: str, db: Session = Depends(get_db)):
    # Fetch the payment details by tracking_id
    payment_detail = db.query(models.PaymentDetails).filter(models.PaymentDetails.tracking_id == tracking_id).first()

    if not payment_detail or not payment_detail.bill_copy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill copy not found")

    # Serve the bill file
    return FileResponse(payment_detail.bill_copy, media_type='application/pdf', filename=f"{tracking_id}_bill.pdf")

