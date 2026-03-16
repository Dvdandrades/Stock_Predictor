from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from datetime import date

from stock_predictor.dependencies.database import get_db
from stock_predictor.stock import schemas, service, crud
from stock_predictor.dependencies.auth import get_current_user

router = APIRouter()


@router.post("/data", status_code=201, response_model=list[schemas.StockData])
async def upload_historical_data(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    list_data = service.parse_csv(file)
    if not list_data:
        raise HTTPException(status_code=404, detail="No data available")
    crud.create_stock_data(list_data, db)
    return list_data


@router.get("/predict", status_code=200, response_model=list[schemas.StockPrediction])
async def get_predictions(
    symbol: str,
    date_start: date,
    date_end: date,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        stock = crud.get_stock_data(
            db=db, symbol=symbol, date_start=date_start, date_end=date_end
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    prediction = service.predict_stock_price(stock_data=stock)
    return prediction


@router.get("/trends", status_code=200, response_model=schemas.StockTrends)
async def get_trends(
    symbol: str,
    date_start: date,
    date_end: date,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        stock = crud.get_stock_data(
            db=db, symbol=symbol, date_start=date_start, date_end=date_end
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    trends = service.get_stock_trends(stock_data=stock)
    return trends


@router.get("/visualize", status_code=200, response_model=list[schemas.StockData])
async def get_data(
    symbol: str,
    date_start: date,
    date_end: date,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        stock = crud.get_stock_data(
            db=db, symbol=symbol, date_start=date_start, date_end=date_end
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return stock
