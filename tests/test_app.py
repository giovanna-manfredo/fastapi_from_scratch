from http import HTTPStatus

from src.schemas import SchemaUser


def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "alice", "email": "alice@example.com"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"username": "alice", "email": "alice@example.com"}


def test_read_users_with_users(client, user):
    user_schema = SchemaUser.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == [user_schema]


def test_read_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == []
