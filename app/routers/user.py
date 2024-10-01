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


@router.get('/profile/{user_id}', response_model=schemas.ShowUser)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    user_data = user.get_user(user_id=user_id, db=db)  # Use the instance to call get_user
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data  # Return the retrieved user data

@router.put('/profile/{user_id}', response_model=schemas.ShowUser)
def update_user_profile(user_id: int, request: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = user.update_user(user_id, request, db)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user