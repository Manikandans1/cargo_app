from sqlalchemy.orm import Session
from .. import models, schemas
from fastapi import HTTPException, status
from .. hashing import Hash
from datetime import datetime


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