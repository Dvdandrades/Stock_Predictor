from sqlalchemy.orm import Session
from stock_predictor.user import models, schemas


def get_user_by_id(db: Session, user_id: int) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.id == user_id, models.User.is_active)
        .first()
    )


def get_user_by_username(db: Session, username: str) -> models.User:
    return (
        db.query(models.User)
        .filter(models.User.username == username, models.User.is_active)
        .first()
    )


def create_user(
    db: Session, user: schemas.UserCreate, hashed_password: str
) -> models.User:
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: models.User, updates: dict) -> models.User:
    for key, value in updates.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_email_in_db(db: Session, email: str) -> bool:
    return db.query(models.User).filter(models.User.email == email).first() is not None


def check_username_in_db(db: Session, username: str) -> bool:
    return (
        db.query(models.User).filter(models.User.username == username).first()
        is not None
    )
