from sqlalchemy.orm.session import Session
from db.models import DBUser
from routers.schemas import UserBase
from db.hashing import Hashing


# Create a new user in the database with the provided data
def db_create_user(db: Session, request: UserBase):
    new_user = DBUser(
        username=request.username,
        email=request.email,
        password=Hashing.hash_password(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"User {new_user.username} created with id {new_user.id}")
    return new_user


# Get a user by ID
def db_get_user_by_id(db: Session, user_id: int):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    return user


# Get a user by username
def get_user_by_username(db: Session, username: str):
    user = db.query(DBUser).filter(DBUser.username == username).first()
    return user