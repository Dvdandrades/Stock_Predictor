from sqlalchemy.orm import Session

from stock_predictor.feedback import crud, schemas


def save_feedback(db: Session, feedback: schemas.FeedbackBase, user_id: int):
    return crud.create_feedback(db=db, feedback=feedback, user_id=user_id)
