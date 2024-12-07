from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from .. import models, schemas
from ..hashing import Hash  # Make sure this points to the correct hashing utility

# Function to create a new user
def create(request: schemas.User, db: Session):
    # Automatically detect the month and year at the time of signup
    current_month = datetime.now().strftime('%B')  # e.g., 'October'
    current_year = datetime.now().year  # e.g., 2024

    # Check if the user_number already exists
    existing_user = db.query(models.User).filter(models.User.user_number == request.user_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User number already registered")

    # Create a new user instance
    new_user = models.User(
        user_name=request.user_name,
        user_number=request.user_number,
        user_password=Hash.bcrypt(request.user_password),  # Hash the password
        signup_month=current_month,
        signup_year=current_year
    )
    
    # Add to the database session and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Return the newly created user as a schema instance (if required)
    return {
        "id": new_user.id,
        "user_name": new_user.user_name,
        "user_number": new_user.user_number,
        "signup_month": new_user.signup_month,
        "signup_year": new_user.signup_year,
        "is_active": new_user.is_active
    }

# Function to show user details by ID
def show(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user