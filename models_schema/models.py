
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users_info'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(300), nullable=False)
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  


class Posts(Base):
    __tablename__ = "user_posts"

    id = Column(Integer, primary_key= True, autoincrement= True, nullable= False, unique= True)
    post_title = Column(String(250),nullable = False)
    post_details = Column(String(500), nullable = False)
    post_it = Column(Boolean, nullable = False, server_default='True')
    created_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id  = Column(Integer, ForeignKey("users_info.id", ondelete="CASCADE"), nullable=False)  # this is to make a bridge between python models classes and treat owner as python object

    # this is to make a bridge between python models classes and treat owner as python object
    owner = relationship("Users", backref="posts")

class Likes(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users_info.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("user_posts.id", ondelete="CASCADE"), primary_key=True)

