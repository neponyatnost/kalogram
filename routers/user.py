import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from db.models import DBUser
from routers.schemas import UserBase, UserDisplay
from db.database import get_db
from db.db_user import db_create_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


# Define a route for the user creation endpoint
@router.post("/", response_model=UserDisplay, summary="Create a new user", description="Create a new user in the database with the provided data")
def create_user(request: UserBase, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user_email = db.query(DBUser).filter(DBUser.email == request.email).first()
    existing_user_username = db.query(DBUser).filter(DBUser.username == request.username).first()

    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    elif existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists"
        )

    new_user = db_create_user(db, request)
    return new_user


# Define a router for getting a user by ID
@router.get("/id/{user_id}", response_model=UserDisplay, summary="Get a user by ID", description="Get a user by ID from the database")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


# Define a router for getting a user by username
@router.get("/username/{username}", response_model=UserDisplay, summary="Get a user by username", description="Get a user by username from the database")
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user