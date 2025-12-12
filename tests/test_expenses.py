import pytest


async def register_and_login(client, email: str, password: str = "password123") -> str:
    await client.post("/api/v1/auth/register", json={"email": email, "password": password})
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return token


@pytest.mark.asyncio
async def test_expense_flow_and_permissions(client):
    token_a = await register_and_login(client, "user_a@example.com")
    token_b = await register_and_login(client, "user_b@example.com")

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Usuário A cria categoria e despesa
    cat_resp = await client.post("/api/v1/categories/", json={"name": "Moradia"}, headers=headers_a)
    assert cat_resp.status_code == 201, cat_resp.text
    category_id = cat_resp.json()["id"]

    exp_payload = {
        "title": "Aluguel",
        "amount": 1500.0,
        "date": "2024-01-10T00:00:00",
        "category_id": category_id,
        "description": "Janeiro",
    }
    exp_resp = await client.post("/api/v1/expenses/", json=exp_payload, headers=headers_a)
    assert exp_resp.status_code == 201, exp_resp.text
    expense_id = exp_resp.json()["id"]

    # Usuário B tenta acessar despesa de A
    forbidden_resp = await client.get(f"/api/v1/expenses/{expense_id}", headers=headers_b)
    assert forbidden_resp.status_code == 404

    # Resumo mensal do usuário A
    summary_resp = await client.get(
        "/api/v1/expenses/summary/monthly?month=1&year=2024",
        headers=headers_a,
    )
    assert summary_resp.status_code == 200
    summary = summary_resp.json()
    assert summary["total"] == pytest.approx(1500.0)
    assert summary["by_category"][0]["category"] == "Moradia"
