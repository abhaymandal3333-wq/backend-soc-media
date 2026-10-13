from fastapi import APIRouter, status, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from database.db import get_db
from oauth2_utils import get_current_user
from schemas.likes_schema import LikesOptions
from models_schema import models



router = APIRouter(
    prefix='/likes',
    tags =['likes']
)

@router.post("/{post_id}/", status_code=status.HTTP_200_OK)
def like_post(post_id:int, likes: LikesOptions | None = None, db:Session = Depends(get_db), user=Depends(get_current_user) ):

    try:
        post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching post from database")

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} does not exist")

    
    liked_post =  db.query(models.Likes).filter(models.Likes.user_id == user.id, models.Likes.post_id == post_id).first()
    if not liked_post and (likes is None or likes.value == 1):
        new_like = models.Likes(user_id=user.id, post_id=post_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)

        return Response(status_code=status.HTTP_201_CREATED, content=f"you liked the {post_id} post")

    elif liked_post and likes.value ==0:
        db.query(models.Likes).filter(models.Likes.user_id == user.id, models.Likes.post_id == post_id).delete()
        db.commit()
        return Response(status_code=status.HTTP_200_OK, content= f"you unliked the {post_id} post")
    
    elif liked_post and (likes is None or likes.value == 1):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"you have already liked the {post_id} post")

    elif not liked_post and likes.value == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"you have not liked the {post_id} post yet")

    
    


@router.get("/count/{post_id}/", status_code=status.HTTP_200_OK)
def get_likes_count(post_id:int, db:Session = Depends(get_db), user=Depends(get_current_user) ):
    try:
        post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching post from database")
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} does not exist")

    try:
        count = db.query(models.Likes).filter(models.Likes.post_id == post_id).count()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching likes count from database")

    return {"post_id": post_id, "likes_count": count}

@router.get("/likedby/{post_id}/", status_code=status.HTTP_200_OK)
def get_users_who_liked_post(post_id:int, db:Session = Depends(get_db), user=Depends(get_current_user) ):
    try:
        post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching post from database")
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} does not exist")
    
    try:
        liked_users = db.query(models.Users.email).select_from(models.Likes).outerjoin(models.Users, models.Likes.user_id == models.Users.id).filter(models.Likes.post_id == post_id).all()
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error fetching liked users from database")

    return {"post_id": post_id, "liked_users": [user.email for user in liked_users]}

