from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_comment import db_create_comment, db_get_all_comments
from routers.schemas import CommentBase, User


router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


# Define a route for the comment creation endpoint
@router.post("/new", summary="Create a new comment", description="Create a new comment in the database with the provided data")
def create_comment(request: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not request.text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Comment text is required"
        )

    new_comment = db_create_comment(db, request)
    return new_comment


# Define a route for getting all comments
@router.get("/all/{post_id}", summary="Get all comments", description="Get all comments for a post from the database")
def get_all_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db_get_all_comments(db, post_id)
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No comments found"
        )
    return comments