from typing import AsyncGenerator
import pytest
import httpx
import os
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.main import app
from app.db.base import Base
from app.db import session as db_session
from app.models.parking_lot import ParkingLot
from app.models.user import User

TEST_DB_URL = os.getenv(
    "DATABASE_URL_TEST",
    "postgresql+asyncpg://app:IboIsIbrahim@localhost:5432/app_test_db",
)
engine = create_async_engine(TEST_DB_URL, future=True)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
def anyio_backend():
    # this tells pytest-anyio: run tests only with asyncio, not trio
    return "asyncio"


@pytest.fixture
async def async_client() -> AsyncGenerator[httpx.AsyncClient, None]:
    # 1. create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. override dependency, capturing THIS sessionmaker
    async def override_get_db():
        async with TestingSessionLocal() as s:
            yield s

    app.dependency_overrides[db_session.get_session] = override_get_db

    # 3. create client with ASGI transport
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # 4. cleanup
    app.dependency_overrides.clear()
    await engine.dispose()


@pytest.fixture
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def user_in_db(async_session: AsyncSession):
    email = "test@test.com"
    user = User(
        username="TestUser",
        password_hash="test",
        name="Test",
        email=email,
        phone="683713498",
        role="User",
        active=True,
        birth_year=2001,
    )
    # check if it already exists
    result = await async_session.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user:
        return user

    async_session.add(user)
    await async_session.flush()  # gets user.id
    await async_session.commit()
    return user


@pytest.fixture
async def lot_in_db(async_session: AsyncSession):
    lot = ParkingLot(name="ParkingLot Test", timezone="CET")
    async_session.add(lot)
    await async_session.flush()
    await async_session.commit()
    return lot
