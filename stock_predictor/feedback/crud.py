from sqlalchemy.orm import Session
from stock_predictor.feedback import models, schemas


def create_feedback(
    db: Session, feedback: schemas.FeedbackBase, user_id: int
) -> models.Feedback:
    db_feedback = models.Feedback(
        subject=feedback.subject, message=feedback.message, user_id=user_id
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
