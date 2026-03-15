from sqlalchemy.orm import Session
from sqlalchemy import insert
from stock_predictor.stock import schemas, models
from datetime import date


def create_stock_data(csv_file: list[schemas.StockData], db: Session) -> None:
    csv_dict = [m.model_dump() for m in csv_file]
    db.execute(insert(models.Stock), csv_dict)
    db.commit()


def get_stock_data(
    db: Session, symbol: str, date_start: date, date_end: date
) -> list[models.Stock]:
    return (
        db.query(models.Stock)
        .filter(
            models.Stock.symbol == symbol,
            models.Stock.date_stamp >= date_start,
            models.Stock.date_stamp <= date_end,
        )
        .all()
    )
