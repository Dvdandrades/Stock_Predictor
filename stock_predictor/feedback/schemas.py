from pydantic import BaseModel, ConfigDict
from datetime import date


class FeedbackBase(BaseModel):
    subject: str
    message: str


class FeedbackOutput(FeedbackBase):
    id: int
    user_id: int
    created_at: date

    model_config = ConfigDict(from_attributes=True)
