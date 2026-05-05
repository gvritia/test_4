def test_list_products_returns_seeded_records(client):
    response = client.get("/products")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 2
    assert payload[0]["description"]


def test_get_existing_product_returns_200(client):
    response = client.get("/products/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Keyboard"


def test_get_missing_product_returns_404(client):
    response = client.get("/products/999")

    assert response.status_code == 404
    assert response.json()["error"] == "product_not_found"


def test_create_product_returns_201(client):
    response = client.post(
        "/products",
        json={
            "title": "Monitor",
            "price": "24999.99",
            "count": 5,
            "description": "27-inch IPS monitor for development tasks.",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Monitor"
    assert payload["description"]

