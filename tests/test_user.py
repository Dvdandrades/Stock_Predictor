def test_signup(mock_client) -> None:
    response = mock_client.post("/user/signup", json={"username": "foo", "email": "foo@foo.com", "password": "foopassword"},)
    assert response.status_code == 201
    assert response.json() == {
        "username": "foo",
        "email": "foo@foo.com"
    }