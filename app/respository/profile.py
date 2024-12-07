from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from .. hashing import Hash
from datetime import datetime


def get_user(user_number: int, db: Session):
        return db.query(models.User).filter(models.User.user_number == user_number).first()

def update_user(user_number: int, request: schemas.UserUpdate, db: Session):
        user = db.query(models.User).filter(models.User.user_number == user_number).first()
        if user:
            user.user_name = request.user_name
            user.user_number = request.user_number
            db.commit()
            db.refresh(user)
            return user
        return None