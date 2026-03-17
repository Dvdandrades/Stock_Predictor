import io
import csv
import datetime


def test_upload_historical_data(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(
        ["symbol", "date_stamp", "time_stamp", "open", "high", "low", "close", "volume"]
    )
    writer.writerow(
        ["DIB", "2016-06-30", "14:30:00", "5.03", "5.12", "5.03", "5.11", "6171340"]
    )
    csv_content = f.getvalue()
    response = mock_client.post(
        "/stock/data",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    assert response.status_code == 201
    assert response.json() == [
        {
            "symbol": "DIB",
            "date_stamp": "2016-06-30",
            "time_stamp": "14:30:00",
            "open": 5.03,
            "high": 5.12,
            "low": 5.03,
            "close": 5.11,
            "volume": 6171340,
        }
    ]


def test_upload_historical_data_error(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    csv_content = "symbol,date_stamp,open,high,low,close,volume"
    response = mock_client.post(
        "/stock/data",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"},
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No data available"}


def test_get_predictions(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    token = login_response.json()["access_token"]
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(
        ["symbol", "date_stamp", "time_stamp", "open", "high", "low", "close", "volume"]
    )
    start_date = datetime.date(2016, 1, 1)
    for i in range(125):
        current_date = start_date + datetime.timedelta(days=i)
        writer.writerow(
            [
                "DIB",
                current_date.strftime("%Y-%m-%d"),
                "14:30:00",
                5.0 + (i * 0.01),
                5.1 + (i * 0.01),
                4.9 + (i * 0.01),
                5.05 + (i * 0.01),
                6000000,
            ]
        )
    csv_content = f.getvalue()
    mock_client.post(
        "/stock/data",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    response = mock_client.get(
        "/stock/predict",
        params={"symbol": "DIB", "date_start": "2016-01-01", "date_end": "2016-03-01"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json()[0]["predicted_price"], float)
    assert response.json()[0]["predicted_price"] > 0


def test_get_trends(mock_client):
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    token = login_response.json()["access_token"]
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(
        ["symbol", "date_stamp", "time_stamp", "open", "high", "low", "close", "volume"]
    )
    writer.writerow(
        ["DIB", "2016-06-30", "14:30:00", "5.03", "5.12", "5.03", "5.11", "6171340"]
    )
    csv_content = f.getvalue()
    mock_client.post(
        "/stock/data",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    response = mock_client.get(
        "/stock/trends",
        params={"symbol": "DIB", "date_start": "2016-06-30", "date_end": "2016-06-30"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "symbol": "DIB",
        "date_range_start": "2016-06-30",
        "date_range_end": "2016-06-30",
        "average_close_price": 5.11,
        "average_volume": 6171340,
        "min_price_period": 5.03,
        "max_price_period": 5.12,
    }


def test_visualize(mock_client):
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    token = login_response.json()["access_token"]
    f = io.StringIO()
    writer = csv.writer(f)
    writer.writerow(
        ["symbol", "date_stamp", "time_stamp", "open", "high", "low", "close", "volume"]
    )
    writer.writerow(
        ["DIB", "2016-06-30", "14:30:00", "5.03", "5.12", "5.03", "5.11", "6171340"]
    )
    csv_content = f.getvalue()
    mock_client.post(
        "/stock/data",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.csv", csv_content, "text/csv")},
    )
    response = mock_client.get(
        "/stock/visualize",
        params={"symbol": "DIB", "date_start": "2016-06-30", "date_end": "2016-06-30"},
        headers={"Authorization": f"Bearer {token}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data[0]["symbol"] == "DIB"
    assert data[0]["close"] == 5.11
