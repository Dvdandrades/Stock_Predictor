import pandas as pd

from pydantic import TypeAdapter
from fastapi import UploadFile

from stock_predictor.stock import schemas

def parse_csv(upload_file: UploadFile) -> list[schemas.StockData]:
    csv_file_adapter = TypeAdapter(list[schemas.StockData])

    df = pd.read_csv(upload_file.file)
    json_file = df.to_json(orient='records')
    return csv_file_adapter.validate_json(json_file)