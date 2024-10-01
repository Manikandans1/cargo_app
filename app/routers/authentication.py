from fastapi import APIRouter, Depends, status,HTTPException
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..hashing import Hash

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login/')
def login(request:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.user_number == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Invalid Credentials")
    if not Hash.verify(user.user_password,request.password):
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"Incorrect password")
    
   
    access_token = token.create_access_token(data={"sub": user.user_number})
    return ({"access_token":access_token, "token_type":"bearer"}) 