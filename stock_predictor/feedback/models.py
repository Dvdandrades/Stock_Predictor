from sqlalchemy import Integer, DateTime, CHAR, Column, String, ForeignKey, func
from stock_predictor.database.session import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    subject = Column(CHAR(500), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(DateTime, server_default=func.now())
    message = Column(String, nullable=False)
