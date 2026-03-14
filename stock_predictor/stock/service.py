import pandas as pd

from pydantic import TypeAdapter
from fastapi import UploadFile
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from stock_predictor.stock import schemas, models


def parse_csv(upload_file: UploadFile) -> list[schemas.StockData]:
    csv_file_adapter = TypeAdapter(list[schemas.StockData])

    df = pd.read_csv(upload_file.file)
    json_file = df.to_json(orient="records")
    return csv_file_adapter.validate_json(json_file)


def predict_stock_price(
    stock_data: list[models.Stock],
) -> list[schemas.StockPrediction]:
    data = [
        {
            "symbol": obj.symbol,
            "date_stamp": obj.date_stamp,
            "close": obj.close,
            "open": obj.open,
            "high": obj.high,
            "low": obj.low,
            "volume": obj.volume,
        }
        for obj in stock_data
    ]
    df = pd.DataFrame(data)
    df.dropna(inplace=True)

    df["SMA_20"] = df["close"].rolling(window=20).mean()
    df["SMA_50"] = df["close"].rolling(window=50).mean()
    df.dropna(inplace=True)

    X = df[["open", "high", "low", "volume", "SMA_20", "SMA_50"]]
    y = df["close"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    test_metadata = df.loc[X_test.index]
    prediction_list = []
    for i in range(len(y_pred)):
        prediction_list.append(
            {
                "symbol": test_metadata.iloc[i]["symbol"],
                "date_stamp": test_metadata.iloc[i]["date_stamp"],
                "predicted_price": y_pred[i],
            }
        )

    prediction_adapter = TypeAdapter(list[schemas.StockPrediction])
    return prediction_adapter.validate_python(prediction_list)
