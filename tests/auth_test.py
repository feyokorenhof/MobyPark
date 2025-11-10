from httpx import AsyncClient
import pytest

EMAIL = "test@test.com"
USERNAME = "test"
NAME = "test"
PASSWORD = "password"
TOKEN_TYPE = "bearer"


@pytest.mark.anyio
async def test_register(async_client: AsyncClient):
    resp = await async_client.post(
        "/auth/register",
        json={
            "email": EMAIL,
            "password": PASSWORD,
            "name": NAME,
            "username": "testuser",
            "phone": "0612345678",
            "role": "user",
            "active": True,
            "birth_year": 1990,
        },
    )
    assert resp.status_code == 201 or resp.status_code == 409
    if resp.status_code == 409:
        return
    data = resp.json()
    assert data["email"] == EMAIL
    assert data["name"] == NAME
    assert "id" in data


@pytest.mark.anyio
async def test_login(async_client: AsyncClient):
    # make sure user exists
    await async_client.post(
        "/auth/register",
        json={"email": EMAIL, "name": NAME, "password": PASSWORD},
    )

    resp = await async_client.post(
        "/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == TOKEN_TYPE
    assert "access_token" in data
