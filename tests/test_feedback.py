def test_feedback(mock_client) -> None:
    mock_client.post(
        "/user/signup",
        json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},
    )
    login_response = mock_client.post(
        "/user/login",
        json={"username": "foo", "password": "foopassword"},
    )
    response = mock_client.post(
        "/feedback",
        headers={"Authorization": f"Bearer {login_response.json()['access_token']}"},
        json={"subject": "foosubject", "message": "foomessage"},
    )

    data = response.json()
    assert response.status_code == 201
    assert data["id"] == 1
    assert data["user_id"] == 1
