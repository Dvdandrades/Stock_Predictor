from pydantic import BaseModel, ConfigDict
from datetime import date, time


class StockData(BaseModel):
    symbol: str
    date_stamp: date
    time_stamp: time
    open: float
    high: float
    low: float
    close: float
    volume: int

    model_config = ConfigDict(from_attributes=True)


class StockPrediction(BaseModel):
    predicted_price: float
    symbol: str
    date_stamp: date


class StockTrends(BaseModel):
    symbol: str
    date_range_start: date
    date_range_end: date
    average_close_price: float
    average_volume: float
    min_price_period: float
    max_price_period: float
