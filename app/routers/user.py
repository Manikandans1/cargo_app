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
@router.post('/register/',response_model=schemas.Show_user)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request,db)



@router.get('/register/{id}',response_model=schemas.Show_user)
def get_user(id:int, db: Session = Depends(get_db)):
    return user.show(id,db)
