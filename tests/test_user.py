import re
from stock_predictor.user.models import User
from tests.conftest import mock_session


def test_signup(mock_client) -> None:
    response = mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    assert response.status_code == 201
    assert response.json() == {"username": "foo", "email": "foo@foo.com"}


def test_signup_error(mock_client) -> None:
    mock_client.post(
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
    mock_client.post(
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


def test_login_error(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    response = mock_client.post(
        "/user/login",
        json={"username": "wrongfoo", "password": "foopassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_get_profile(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    response = mock_client.get(
        "/user/profile",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json() == {"username": "foo", "email": "foo@foo.com"}


def test_get_profile_error_token(mock_client) -> None:
    response = mock_client.get("/user/profile")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_get_profile_inactive_user(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    db = mock_session()
    user = db.query(User).filter(User.username == "foo").first()
    user.is_active = False
    db.commit()
    db.close()
    response = mock_client.get(
        "/user/profile",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Inactive user"}


def test_get_profile_user_not_found(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    db = mock_session()
    user = db.query(User).filter(User.username == "foo").first()
    user.username = "newfoo"
    db.commit()
    db.close()
    response = mock_client.get(
        "/user/profile",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "User not found"}


def test_update_profile(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    response = mock_client.put(
        "/user/profile",
        json={
            "username": "newfoo",
            "email": "newfoo@foo.com",
            "password": "newfoopassword",
        },
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == "newfoo"
    assert data["email"] == "newfoo@foo.com"
