from pydantic import BaseModel, ConfigDict
from datetime import datetime


class FeedbackBase(BaseModel):
    subject: str
    message: str


class FeedbackOutput(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
