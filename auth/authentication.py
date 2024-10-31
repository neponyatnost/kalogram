from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session
from auth.oauth2 import create_access_token
from db.database import get_db
from db.hashing import Hashing
from db.models import DBUser


# Create API router instance
router = APIRouter(
    tags=["authentication"],
)


# Define a route for the login endpoint
@router.post("/login", summary="Login", description="Login with the provided credentials")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    if not Hashing.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    access_token = create_access_token(data={
        'username': user.username,
    })
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username,
    }