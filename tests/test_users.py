from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "password": "password",
            "email": "test@test.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "testusername",
        "email": "test@test.com",
    }


def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "123",
            "id": 1,
            "username": "testusername2",
            "email": "test@test.com",
        },
    )
    assert response.json() == {
        "id": 1,
        "username": "testusername2",
        "email": "test@test.com",
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.json() == {"message": "User deleted successfully"}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "You don't have permission to access this user"
    }


def test_update_wrong_user(client, other_user, token):
    response = client.put(
        f"/users/{other_user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "password": "123",
            "id": 1,
            "username": "testusername2",
            "email": "test2@gmail.com",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "You don't have permission to access this user"
    }


def test_create_user_with_existing_email(client, user):
    response = client.post(
        "/users/",
        json={
            "username": "testusername",
            "password": "password",
            "email": user.email,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Email already exists"}


def test_create_user_with_existing_username(client, user):
    response = client.post(
        "/users/",
        json={
            "username": user.username,
            "password": "password",
            "email": "test@gmail.com",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Username already exists"}
