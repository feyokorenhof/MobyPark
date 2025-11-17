from httpx import AsyncClient
import pytest

EMAIL = "test@test.com"
USERNAME = "test"
NAME = "test"
PASSWORD = "password"
TOKEN_TYPE = "bearer"


@pytest.mark.anyio
async def test_register_valid(async_client: AsyncClient):
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
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == EMAIL
    assert data["name"] == NAME
    assert "id" in data


@pytest.mark.anyio
async def test_register_existing(async_client: AsyncClient):
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
    # Expect 409 (conflict) because user already exists
    assert resp.status_code == 409


@pytest.mark.anyio
async def test_register_bad_email(async_client: AsyncClient):
    resp = await async_client.post(
        "/auth/register",
        json={
            "email": "hi",
            "password": PASSWORD,
            "name": NAME,
            "username": "testuser",
            "phone": "0612345678",
            "role": "user",
            "active": True,
            "birth_year": 1990,
        },
    )
    # Expect 422 (Unprocessable Entry) because email is invalid
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_login_valid(async_client: AsyncClient):
    resp = await async_client.post(
        "/auth/login",
        json={"email": EMAIL, "password": PASSWORD},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["token_type"] == TOKEN_TYPE
    assert "access_token" in data


@pytest.mark.anyio
async def test_login_invalid(async_client: AsyncClient):
    resp = await async_client.post(
        "/auth/login",
        json={"email": "invalid@gmail.com", "password": "invalid"},
    )
    # Expect 401 (Unauthorized) because user doesn't exist
    assert resp.status_code == 401
