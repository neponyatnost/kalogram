import datetime
from sqlalchemy.orm.session import Session

from db.models import DBComment
from routers.schemas import CommentBase


def db_create_comment(db: Session, request: CommentBase):
    new_comment = DBComment(
        text=request.text,
        username=request.username,
        post_id=request.post_id,
        creator_id=request.user_id,
        timestamp=datetime.datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def db_get_all_comments(db: Session, post_id: int):
    comments = db.query(DBComment).filter(DBComment.post_id == post_id).all()
    return comments


def db_delete_comment():
    pass


def db_get_comments_by_post_id():
    pass


def db_get_comments_by_user_id():
    pass


def db_get_comment_by_id():
    pass


def db_update_comment():
    pass