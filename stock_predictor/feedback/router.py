from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from stock_predictor.feedback import schemas, service
from stock_predictor.dependencies.auth import get_current_user
from stock_predictor.dependencies.database import get_db

router = APIRouter()


@router.post("/feedback", status_code=201, response_model=schemas.FeedbackOutput)
def post_feedback(
    feedback: schemas.FeedbackBase,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    feedback = service.save_feedback(db=db, feedback=feedback, user_id=current_user.id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback data not available")
    return feedback
