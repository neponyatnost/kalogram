import shutil
import uuid
from fastapi import APIRouter, Depends, status, UploadFile, File
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_post import db_create_post, db_delete_post, db_get_all_posts
from db.models import DBPost
from routers.schemas import PostBase, PostDisplay, User


# Create API router instance
router = APIRouter(
    prefix="/posts",
    tags=["posts"],
)


# Define the allowed image URL types
image_url_types = ['absolute', 'relative']


# Define a route for the post creation endpoint
@router.post("/new", response_model=PostDisplay, summary="Create a new post", description="Create a new post in the database with the provided data")
def create_post(request: PostBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid image URL type. Must be one of: 'absolute', 'relative'"
        )
    new_post = db_create_post(db, request)
    return new_post


# Define a route for getting all posts
@router.get("/all", response_model=list[PostDisplay], summary="Get all posts", description="Get all posts from the database")
def get_all_posts(db: Session = Depends(get_db)):
    posts = db_get_all_posts(db)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No posts found"
        )
    return posts


# Upload an image file for a post
@router.post('/image', summary="Upload an image file", description="Upload an image file for a post")
def upload_post_image(image: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Accept only images
    if not image.filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid file type. Only images are allowed')

    # Maximum file size: 3MB
    max_size = 3 * 1024 * 1024

    if image.size > max_size:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='File size is too large')

    unique_filename = str(uuid.uuid4()) + '_' + image.filename

    path = f'images/{unique_filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)

    return {"filename": path}


# Define a route for deleting a post
@router.get("/delete/{post_id}", summary="Delete a post", description="Delete a post by ID")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_to_delete = db.query(DBPost).filter(DBPost.id == post_id).first()
    if post_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    if post_to_delete.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this post"
        )
    return db_delete_post(db, post_to_delete.id, current_user.id)