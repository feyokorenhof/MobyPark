import os
import asyncio
import pytest
import httpx
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import session
from app.db.base import Base
from app.main import app


TEST_DB_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://app:IboIsIbrahim@localhost:5432/app_db_test",
)
engine = create_async_engine(TEST_DB_URL, future=True)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[session.get_session] = override_get_db


@pytest.fixture(scope="session", autouse=True)
def create_test_db_schema():
    """
    Create all tables in the test database once before any tests run.
    """

    async def _create():
        async with engine.begin() as conn:
            # this creates all tables defined on Base.metadata
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_create())
    # yield so tests can run afterwards
    yield
    # optional: drop tables after tests
    # asyncio.run(_drop())


@pytest.fixture
async def async_client():
    # this is the new way: build an ASGI transport for httpx
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


email = "test@test.com"
name = "test"
password = "password"
token_type = "bearer"


@pytest.mark.anyio
async def test_register(async_client):
    resp = await async_client.post(
        "/auth/register",
        # headers={"X-Token": "coneofsilence"},
        json={"email": email, "name": name, "password": password},
    )
    assert resp.json() == {"id": resp.json()["id"], "email": email, "name": name}


@pytest.mark.anyio
async def test_login(async_client):
    resp = await async_client.post(
        "/auth/login",
        headers={"X-Token": "coneofsilence"},
        json={"email": email, "password": password},
    )
    assert resp.json() == {
        "token": resp.json()["access_token"],
        "token_type": token_type,
    }
