from fastapi import FastAPI, HTTPException, status, Depends
from models_schema import models  
from database.db import engine
from router import users, posts, auth , likes


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(likes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to user posts api"}











    