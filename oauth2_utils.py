from datetime import datetime, timedelta
from jose import JWTError, jwt
from schemas import token_schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.db import get_db
from models_schema import models
from config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.expiration_time

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = EXPIRATION_TIME)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = payload["user_id"]
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    token_data = token_schema.TokenData(id = user_id)
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)): 
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    return user


if __name__ == "__main__":
    print(create_access_token({"user_id":1}))
    print("hello")
    #print(verify_access_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE3ODg1MjQzNjh9.dlDYbp7Rn6Q5aboYyqt8AP3_CDhzqvGj56Fij-RxdHQ", HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")))
    
    print(get_current_user("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo3LCJleHAiOjE3ODk2NDM0MjR9.DcTdAI_pu4rnhMAU3_wXsAdmWoDN_cn9p6cgagC3G6A",db))




