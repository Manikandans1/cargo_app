from fastapi import APIRouter
from .. import database, schemas, models
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..respository import profile


router = APIRouter(
    tags=['Profile']
)
get_db = database.get_db

# Route to get the user profile based on user_number
@router.get('/profile/{user_number}', response_model=schemas.ShowUser)
def get_user_profile(user_number: str, db: Session = Depends(get_db)):
    user_data = profile.get_user(user_number=user_number, db=db)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

# Route to update the user profile based on user_number
@router.put('/profile/{user_number}', response_model=schemas.ShowUser)
def update_user_profile(user_number: str, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = profile.update_user(user_number=user_number, request=request, db=db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
