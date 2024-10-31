from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr


# User Schema for the user creation endpoint
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


# User Schema for the user display endpoint
class UserDisplay(BaseModel):
    username: str
    email: str

    class ConfigDict:
        from_attributes = True


# Comment Schema for the comment display endpoint
class CommentDisplay(BaseModel):
    username: str
    text: str
    timestamp: datetime

    class ConfigDict:
        from_attributes = True


# User schema for Post display endpoint
class User(BaseModel):
    id: int
    username: str
    email: str

    class ConfigDict:
        from_attributes = True


# Post Schema for the post creation endpoint
class PostBase(BaseModel):
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int


# Post Schema for the post display endpoint
class PostDisplay(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    creator_id: int
    timestamp: datetime
    user: User
    comments: List[CommentDisplay]

    class ConfigDict:
        from_attributes = True


# Comment Schema for the comment creation endpoint
class CommentBase(BaseModel):
    post_id: int
    user_id: int
    username: str
    text: str


