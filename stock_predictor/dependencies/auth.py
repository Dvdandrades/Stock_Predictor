from fastapi import Depends, HTTPException, status
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
    user = (
        db.query(models.User)
        .filter(models.User.username == token_data.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )

    return user
