from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from stock_predictor.user import models
from stock_predictor.auth import jwt
from stock_predictor.dependencies.database import get_db


security = HTTPBearer()


def get_current_user(
    db: Session = Depends(get_db),
    auth: HTTPAuthorizationCredentials = Depends(security),
) -> models.User:
    token = auth.credentials
    token_data = jwt.verify_token(token=token)
    return (
        db.query(models.User)
        .filter(models.User.username == token_data.username, models.User.is_active)
        .first()
    )
