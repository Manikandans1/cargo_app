from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from .. hashing import Hash
from datetime import datetime


def create(request: schemas.User, db: Session):
    
    # Automatically detect the month and year at the time of signup
    current_month = datetime.now().strftime('%B')  # e.g., 'October'
    current_year = datetime.now().year  # e.g., 2024

    new_user = models.User(
        user_name=request.user_name,
        user_number=request.user_number,
        user_password=Hash.bcrypt(request.user_password),  # Hash the password
        signup_month=current_month,
        signup_year=current_year
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"User with the id {id} is not available")
    return user

def get_user(user_id: int, db: Session):
        return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(user_id: int, request: schemas.UserUpdate, db: Session):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.user_name = request.user_name
            user.user_number = request.user_number
            db.commit()
            db.refresh(user)
            return user
        return None