from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from database import db
from models_schema import models
from database.db import engine
from schemas import users
from database.db import get_db
from sqlalchemy.orm import Session
import utils

router = APIRouter(
    prefix="/users",   
    tags=["Users"]
)

# api for the users handling
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=users.UserOutput)
def create_user(user: users.UserInput, db: Session = Depends(get_db)):
    user.password = utils.hash(user.password)
    new_user = models.Users(**dict(user))
    if not new_user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="User not created")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=users.UserOutput)
def user_by_id(id:int, db:Session = Depends(get_db)):
    
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")

    return user
