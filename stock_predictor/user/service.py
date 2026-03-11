import bcrypt

from sqlalchemy.orm import Session

from stock_predictor.user import models, schemas, crud


def signup_user(db: Session, user: schemas.UserCreate) -> models.User:
    if crud.check_email_in_db(db=db, email=user.email) or crud.check_username_in_db(
        db=db, username=user.username
    ):
        raise ValueError("Email and username already exist")
    hashed_password = bcrypt.hashpw(
        user.password.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)


def authenticate_user(db: Session, user: schemas.UserLogin) -> models.User:
    if db_user := crud.get_user_by_username(db=db, username=user.username):
        if bcrypt.checkpw(
            password=user.password.encode("utf-8"),
            hashed_password=db_user.hashed_password,
        ):
            return db_user
    raise ValueError("Invalid credentials")


def update_user_profile(
    db: Session, updates: schemas.UserUpdate, user_id: int
) -> models.User:
    if user := crud.get_user_by_id(db=db, user_id=user_id):
        update_data = updates.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = bcrypt.hashpw(
                update_data.pop("password").encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        return crud.update_user(db=db, db_user=user, updates=update_data)
    raise ValueError("User not found")
