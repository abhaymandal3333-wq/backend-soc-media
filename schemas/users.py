
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserInput(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_time: datetime
    class Config:
        orm_mode = True


