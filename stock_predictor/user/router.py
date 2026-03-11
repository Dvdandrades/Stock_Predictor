from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from stock_predictor.dependencies.database import get_db
from stock_predictor.dependencies.auth import get_current_user
from stock_predictor.user import schemas, service

router = APIRouter()


@router.get("/profile", status_code=200, response_model=schemas.UserBase)
async def get_profile(current_user=Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user


@router.post("/signup", status_code=201, response_model=schemas.UserBase)
async def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return service.signup_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", status_code=200, response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        if service.authenticate_user(db=db, user=user):
            return schemas.Token(access_token="placeholder", token_type="bearer")
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.put("/profile", status_code=200, response_model=schemas.User)
async def update_profile(
    updates: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive User")
    try:
        return service.update_user_profile(
            db=db, updates=updates, user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
