import re


def test_signup(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    assert response.status_code == 201
    assert response.json() == {"username": "foo", "email": "foo@foo.com"}


def test_signup_error(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email and username already exist"}


def test_login(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    token = response.json()["access_token"]
    jwt_pattern = r"^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$"
    assert response.status_code == 200
    assert re.match(jwt_pattern, token)
