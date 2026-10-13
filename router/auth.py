from fastapi import APIRouter,status, HTTPException, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models_schema import models
from utils import hash, verify
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import oauth2_utils
from schemas import token_schema



router = APIRouter(
    prefix='/login',
    tags = ['authentication']
    
)


@router.post("/", status_code = status.HTTP_200_OK, response_model = token_schema.Token )
def login(credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    try:
        user = db.query(models.Users).filter((models.Users.email == credentials.username)).first()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching user from database")

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid credentials")


    if not verify(credentials.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Invalid credentials")

    
    return {"token_type": "bearer","access_token": oauth2_utils.create_access_token({"user_id":user.id})}