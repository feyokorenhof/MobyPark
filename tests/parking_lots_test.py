from httpx import AsyncClient
import pytest

from app.models.parking_lot import ParkingLot


@pytest.mark.anyio
async def test_get_lot(
    async_client: AsyncClient,
    lot_in_db: ParkingLot,
):
    resp = await async_client.get(f"/parking_lots/{lot_in_db.id}")

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == lot_in_db.id


@pytest.mark.anyio
async def test_create_lot(
    async_client: AsyncClient,
):
    resp = await async_client.post(
        "/parking_lots",
        json={
            "name": "TestLot",
            "location": "Rotterdam",
            "address": "Wijnhaven 103",
            "capacity": 20,
            "reserved": 0,
            "tariff": 5.0,
            "daytariff": 30.0,
            "latitude": 51.926517,
            "longitude": 4.462456,
        },
    )

    # Expect 201 (Created)
    assert resp.status_code == 201
