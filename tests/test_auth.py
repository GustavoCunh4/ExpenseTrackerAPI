import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    email = "user@example.com"
    password = "supersecret"

    response = await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == email
    assert "id" in data

    login_response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == 200, login_response.text
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
