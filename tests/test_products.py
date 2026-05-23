"""Синхронные тесты эндпоинтов products.

Относится к заданиям:
- 9.1: проверяем результат миграций и работу ресурса Product;
- 11.1: покрываем основные HTTP-сценарии.
"""


def test_list_products_returns_seeded_records(client):
    # После миграций в таблице уже должны быть 2 стартовые записи.
    response = client.get("/products")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 2
    assert payload[0]["description"]
    assert isinstance(payload[0]["check"], bool)


def test_get_existing_product_returns_200(client):
    # Товар с id=1 создается стартовой миграцией.
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Keyboard"


def test_get_missing_product_returns_404(client):
    # Проверяем кастомную ошибку для несуществующего товара.
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json()["error"] == "product_not_found"


def test_create_product_returns_201(client):
    # Создание товара идет через JSON и валидируется Pydantic-моделью.
    response = client.post(
        "/products",
        json={
            "title": "Monitor",
            "price": "24999.99",
            "count": 5,
            "description": "27-inch IPS monitor for development tasks.",
            "check": True,
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Monitor"
    assert payload["description"]
    assert payload["check"] is True
