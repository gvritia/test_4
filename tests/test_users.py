"""Синхронные тесты users-эндпоинтов.

Относится к заданиям:
- 10.2: проверка валидации пользовательских данных;
- 11.1: проверка разных сценариев через TestClient.
"""


def test_create_user_returns_201_and_public_fields(client):
    # Создаем пользователя и убеждаемся, что в ответе только публичные поля.
    response = client.post(
        "/users",
        json={
            "username": "student_one",
            "age": 22,
            "email": "student_one@example.com",
            "password": "password1",
            "phone": "+79990001122",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] == 1
    assert payload["username"] == "student_one"
    assert "password" not in payload


def test_create_user_returns_409_for_duplicate_username(client):
    # Первый запрос должен пройти успешно, второй - упасть из-за конфликта username.
    payload = {
        "username": "student_one",
        "age": 22,
        "email": "student_one@example.com",
        "password": "password1",
        "phone": "+79990001122",
    }

    first_response = client.post("/users", json=payload)
    second_response = client.post(
        "/users",
        json={**payload, "email": "another@example.com"},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert second_response.json()["error"] == "user_already_exists"


def test_create_user_returns_custom_validation_payload(client):
    # Намеренно передаем несколько неправильных значений,
    # чтобы проверить единый формат 422-ответа.
    response = client.post(
        "/users",
        json={
            "username": "ab",
            "age": 17,
            "email": "wrong-email",
            "password": "123",
        },
    )

    assert response.status_code == 422
    payload = response.json()
    assert payload["error"] == "validation_error"
    assert len(payload["details"]) >= 3


def test_get_missing_user_returns_404(client):
    # Проверяем пользовательскую 404-ошибку.
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["error"] == "user_not_found"
