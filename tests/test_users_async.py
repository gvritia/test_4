import pytest


@pytest.mark.asyncio
async def test_create_user_async_returns_201(async_client, faker):
    response = await async_client.post(
        "/users",
        json={
            "username": faker.user_name(),
            "age": faker.random_int(min=19, max=60),
            "email": faker.email(),
            "password": "password1",
            "phone": faker.numerify(text="+7##########"),
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["id"] == 1
    assert payload["email"]


@pytest.mark.asyncio
async def test_get_existing_user_async_returns_200(async_client, faker):
    create_response = await async_client.post(
        "/users",
        json={
            "username": faker.user_name(),
            "age": faker.random_int(min=19, max=60),
            "email": faker.email(),
            "password": "password1",
            "phone": faker.numerify(text="+7##########"),
        },
    )
    user_id = create_response.json()["id"]

    response = await async_client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


@pytest.mark.asyncio
async def test_get_missing_user_async_returns_404(async_client):
    response = await async_client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["error"] == "user_not_found"


@pytest.mark.asyncio
async def test_delete_existing_user_async_returns_204(async_client, faker):
    create_response = await async_client.post(
        "/users",
        json={
            "username": faker.user_name(),
            "age": faker.random_int(min=19, max=60),
            "email": faker.email(),
            "password": "password1",
            "phone": faker.numerify(text="+7##########"),
        },
    )
    user_id = create_response.json()["id"]

    response = await async_client.delete(f"/users/{user_id}")

    assert response.status_code == 204
    assert response.text == ""


@pytest.mark.asyncio
async def test_delete_same_user_twice_async_returns_404(async_client, faker):
    create_response = await async_client.post(
        "/users",
        json={
            "username": faker.user_name(),
            "age": faker.random_int(min=19, max=60),
            "email": faker.email(),
            "password": "password1",
            "phone": faker.numerify(text="+7##########"),
        },
    )
    user_id = create_response.json()["id"]

    first_response = await async_client.delete(f"/users/{user_id}")
    second_response = await async_client.delete(f"/users/{user_id}")

    assert first_response.status_code == 204
    assert second_response.status_code == 404
    assert second_response.json()["error"] == "user_not_found"
