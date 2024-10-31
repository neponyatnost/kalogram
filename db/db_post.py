from datetime import datetime
from turtle import st
from sqlalchemy.orm.session import Session
from db.models import DBPost
from routers.schemas import PostBase


# Create a new post in the database with the provided data
def db_create_post(db: Session, request: PostBase):
    new_post = DBPost(
        image_url=request.image_url,
        image_url_type=request.image_url_type,
        caption=request.caption,
        creator_id=request.creator_id,
        timestamp=datetime.now(),
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# Get all posts from the database
def db_get_all_posts(db: Session):
    posts = db.query(DBPost).all()
    return posts


# Delete post
def db_delete_post(db: Session, post_id: int, current_user_id: int):
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    db.delete(post)
    db.commit()
    return {
        'message': f'Post with ID {post_id} deleted successfully'
    }