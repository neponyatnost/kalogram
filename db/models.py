from calendar import c
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from .database import Base
from sqlalchemy.orm import relationship


# Define the database model for the user
class DBUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    posts = relationship("DBPost", back_populates="user")


# Define the database model for the post
class DBPost(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String)
    image_url_type = Column(String)
    caption = Column(String)
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("DBUser", back_populates="posts")
    comments = relationship("DBComment", back_populates="post")


# Define the database model for the comment
class DBComment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    username = Column(String)
    timestamp = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    # user = relationship("DBUser")
    post = relationship("DBPost", back_populates="comments")