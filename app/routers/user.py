from fastapi import APIRouter
from .. import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..respository import user



router = APIRouter(
    tags=['User']
)
get_db = database.get_db



#CREATE THE NEW USER
@router.post('/register/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/register/{id}',response_model=schemas.Show_user)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.show(id,db)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
import random
from typing import Dict

from .. import database, schemas, models
from ..respository import user

# router = APIRouter(
#     tags=['User']
# )

get_db = database.get_db

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory storage for OTPs (replace with Redis for production)
otp_store: Dict[str, Dict[str, str]] = {}

# Helper function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Pydantic schema for requesting OTP
class OTPRequest(BaseModel):
    user_number: str

# Pydantic schema for resetting password
class ResetPasswordRequest(BaseModel):
    user_number: str
    otp: str
    new_password: str


# CREATE THE NEW USER
@router.post('/register/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


# GET USER BY ID
@router.get('/register/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)


# Forgot password route: Sends OTP to the user's mobile number
@router.post("/forgot-password/")
async def forgot_password(request: OTPRequest):
    otp = generate_otp()

    # Store OTP in memory with expiration (10 minutes)
    otp_store[request.user_number] = {
        "otp": otp,
        "expires_at": (datetime.now() + timedelta(minutes=10)).isoformat()
    }

    # In production, you'd send this OTP via SMS to the user
    print(f"OTP for {request.user_number}: {otp}")  # For testing purposes only

    return {"message": "OTP has been sent to your mobile number."}


# Reset password route
@router.post("/reset-password/")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    # Check if the OTP exists for the mobile number
    if request.user_number not in otp_store:
        raise HTTPException(status_code=400, detail="OTP not requested or expired")

    otp_data = otp_store[request.user_number]

    # Check if the OTP is expired
    if datetime.now() > datetime.fromisoformat(otp_data["expires_at"]):
        raise HTTPException(status_code=400, detail="OTP has expired")

    # Verify if the provided OTP matches the stored OTP
    if request.otp != otp_data["otp"]:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # Reset the password in the database
    user_instance = db.query(models.User).filter(models.User.user_number == request.user_number).first()

    if not user_instance:
        raise HTTPException(status_code=404, detail="User not found")

    # Hash the new password
    hashed_password = pwd_context.hash(request.new_password)
    user_instance.user_password = hashed_password

    db.commit()

    # Optionally, remove the OTP after successful password reset
    del otp_store[request.user_number]

    return {"message": "Password has been reset successfully"}

#--------OFFER SECTION-----------


from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.responses import StreamingResponse
from io import BytesIO

# Database setup
DATABASE_URL = "postgresql://Embassy:Embassy12@localhost:5432/cargoapp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the Image model
class OfferImage(Base):
    __tablename__ = 'offer_images'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # Optional: To describe the offer
    file_data = Column(LargeBinary)  # Store the image binary data
    content_type = Column(String)  # Store the image's content type (e.g., "image/jpeg")

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# API Endpoint to upload an offer image
@router.post("/upload-offer/")
async def upload_offer_image(
    title: str,  # Title or description of the offer
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Read the image as binary data
        file_data = await file.read()

        # Save the image metadata and binary data to the database
        db_image = OfferImage(
            title=title,
            file_data=file_data,
            content_type=file.content_type  # Save the content type (e.g., "image/jpeg")
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return {"message": "Offer image uploaded successfully", "id": db_image.id, "title": db_image.title}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# API Endpoint to get all offer images
@router.get("/offers/")
async def get_all_offer_images(db: Session = Depends(get_db)):
    try:
        # Query all images from the database
        images = db.query(OfferImage).all()
        if not images:
            raise HTTPException(status_code=404, detail="No offer images found")

        # Return metadata for each image
        return [
            {"id": img.id, "title": img.title}
            for img in images
        ]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API Endpoint to retrieve an offer image by ID
@router.get("/offers/{image_id}")
async def get_offer_image(image_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the image by ID
        db_image = db.query(OfferImage).filter(OfferImage.id == image_id).first()
        if not db_image:
            raise HTTPException(status_code=404, detail="Offer image not found")

        # Return the image as a streaming response
        image_stream = BytesIO(db_image.file_data)
        return StreamingResponse(image_stream, media_type=db_image.content_type)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/offers/{image_id}")
async def delete_offer_image(image_id: int, db: Session = Depends(get_db)):
    try:
        # Fetch the image by ID
        db_image = db.query(OfferImage).filter(OfferImage.id == image_id).first()

        if not db_image:
            raise HTTPException(status_code=404, detail="Offer image not found")

        # Delete the image from the database
        db.delete(db_image)
        db.commit()

        # Optionally, if you're storing files in the local system, you can delete them too:
        # os.remove(f"{UPLOAD_FOLDER}/{db_image.file_name}")  # if you use a folder to store images

        return {"message": "Offer image deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))