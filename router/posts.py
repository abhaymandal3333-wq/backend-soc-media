from fastapi import FastAPI, HTTPException, status, Depends, APIRouter,Response
from database import db
from database.db import engine
from schemas import users, posts
from database.db import get_db
from sqlalchemy.orm import Session
import utils
from oauth2_utils import get_current_user
from schemas import posts
from models_schema import models

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/" , status_code=status.HTTP_200_OK , response_model= list[posts.PostOutput])
def get_all_posts(db:Session = Depends(get_db), user=Depends(get_current_user) ):
   
    # try:
    #     db.cursor.execute("""SELECT * FROM user_posts""")
    #     results = db.cursor.fetchall()
        
    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT FETCHING DATA FROOM DATABASE ")

    # return {"data": [dict(result) for result in results]}

    try:
        all_posts = db.query(models.Posts).all()

    except Exception as error:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT FETCHING DATA FROM DATABASE")
    return list(all_posts)
     

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=posts.PostOutput)
def get_post_by_id(id:int, db:Session = Depends(get_db), user=Depends(get_current_user)):
    # try:
    #     db.cursor.execute("""SELECT * FROM user_posts WHERE id = %s""", (id,))
    #     result = db.cursor.fetchone()
        
    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT FETCHING DATA FROOM DATABASE ")

    # if not result:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"post with id {id} not found")
    
    # return {"data": {'post title': result['post_title'], 'post content': result['post_details'], 'created time': result['created_time']}}

    try:
        result = db.query(models.Posts).filter(models.Posts.id == id).first()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details= "NOT FETCHING DATA FROM DATABASE")

    if not result:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, details=f"post with id {id} not found")
    
    return result

@router.get("/user/{user_id}", status_code=status.HTTP_200_OK, response_model= list[posts.PostOutput])
def get_posts_by_user_id(user_id:int , db:Session = Depends(get_db), user=Depends(get_current_user)):
    if not db.query(models.Users).filter(models.Users.id == user_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with id {user_id} not found")
    try:
        posts = db.query(models.Posts).filter(models.Posts.owner_id == user_id).all()
    except Exception as error:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="NOT FETCHING DATA FROM DATABASE")
    if not posts:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail=f"User {user_id} has not posted yet")
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= posts.PostOutput)
def create_post(post: posts.PostInput, db:Session = Depends(get_db), user= Depends(get_current_user)):
    # try:
    #     db.cursor.execute("""INSERT INTO user_posts (post_title, post_details, post_it) VALUES (%s, %s , %s) RETURNING *""", (post['post_title'], post['post_details'], post['post_it']))
    #     new_post = db.cursor.fetchone()
    #     db.conn.commit()
        
    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT INSERTING DATA INTO DATABASE ")

    # return {"data": {'post title': new_post['post_title'], 'post content': new_post['post_details'], 'created time': new_post['created_time']}}
    
    try:
        new_post = models.Posts(owner_id= user.id, **dict(post))
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT INSERTING DATA INTO DATABASE ")

    return new_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model= posts.PostOutput)
def update_post(id:int, post: posts.PostInput, db:Session = Depends(get_db), user = Depends(get_current_user)):
    # try:
    #     db.cursor.execute("""UPDATE user_posts SET post_title = %s, post_details = %s, post_it = %s WHERE id = %s RETURNING *""", (post['post_title'], post['post_details'], post['post_it'], id))
    #     updated_post = db.cursor.fetchone()
    #     db.conn.commit()
        
    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT UPDATING DATA INTO DATABASE ")

    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"post with id {id} not found")
    
    # return {"data": {'post title': updated_post['post_title'], 'post content': updated_post['post_details'], 'created time': updated_post['created_time']}}

   
    if not db.query(models.Posts).filter(models.Posts.id == id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"post with id {id} not found")
    
    try:
        updated_post = db.query(models.Posts).filter(models.Posts.id == id).update(dict(post))
        db.commit()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, details="NOT UPDATING DATA INTO DATABASE ")

    return db.query(models.Posts).filter(models.Posts.id == id).first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), user= Depends(get_current_user)):
   
    # try:
    #     db.cursor.execute("""DELETE FROM user_posts WHERE id = %s RETURNING *""", (id,))
    #     deleted_post = db.cursor.fetchone()
    #     db.conn.commit()

    # except Exception as error:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="NOT DELETING DATA FROM DATABASE ")


    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")

    if not db.query(models.Posts).filter(models.Posts.id == id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else:
        try:
            db.query(models.Posts).filter(models.Posts.id == id).delete()
            db.commit()
        except Exception as error:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="NOT DELETING DATA FROM DATABASE ")
    return Response(status_code= status.HTTP_200_OK, content=f"post with id {id} deleted successfully")
