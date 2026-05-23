"""Синхронные тесты auth-эндпоинтов.

Относится к заданию 11.1: проверяем успешные и ошибочные сценарии авторизации.
"""


def test_login_returns_token_and_allows_get_current_user(client):
    # Сначала создаем пользователя, иначе логинить будет некого.
    create_response = client.post(
        "/users",
        json={
            "username": "rest_user",
            "age": 25,
            "email": "rest_user@example.com",
            "password": "password1",
            "phone": "+79990001122",
        },
    )
    assert create_response.status_code == 201

    # Логин отправляем через JSON-тело, а не через query string.
    login_response = client.post(
        "/auth/login",
        json={"username": "rest_user", "password": "password1"},
    )

    assert login_response.status_code == 200
    payload = login_response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["authorization_header"] == f"Bearer {payload['access_token']}"

    # Получаем профиль текущего пользователя по Bearer-токену.
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {payload['access_token']}"},
    )

    assert me_response.status_code == 200
    assert me_response.json()["username"] == "rest_user"


def test_login_with_wrong_password_returns_401(client):
    # Создаем пользователя с известным паролем.
    client.post(
        "/users",
        json={
            "username": "rest_user",
            "age": 25,
            "email": "rest_user@example.com",
            "password": "password1",
            "phone": "+79990001122",
        },
    )

    response = client.post(
        "/auth/login",
        json={"username": "rest_user", "password": "wrongpass"},
    )

    # При неверном пароле ожидаем именно 401 Unauthorized.
    assert response.status_code == 401
    assert response.json()["error"] == "unauthorized"


def test_logout_invalidates_token(client):
    # Повторяем жизненный цикл: создать пользователя -> войти -> выйти.
    client.post(
        "/users",
        json={
            "username": "rest_user",
            "age": 25,
            "email": "rest_user@example.com",
            "password": "password1",
            "phone": "+79990001122",
        },
    )
    login_response = client.post(
        "/auth/login",
        json={"username": "rest_user", "password": "password1"},
    )
    token = login_response.json()["access_token"]

    # После logout токен должен перестать работать.
    logout_response = client.delete(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert logout_response.status_code == 204

    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_response.status_code == 401
