from httpx import AsyncClient
import pytest

from app.models.parking_lot import ParkingLot
from app.schemas.parking_lot import ParkingLotIn, ParkingLotOut


@pytest.mark.anyio
async def test_get_lot(
    async_client: AsyncClient, lot_in_db: ParkingLot, auth_headers_user: dict[str, str]
):
    resp = await async_client.get(
        f"/parking_lots/{lot_in_db.id}", headers=auth_headers_user
    )

    assert resp.status_code == 200
    data = ParkingLotOut.model_validate(resp.json())
    assert data.id == lot_in_db.id


@pytest.mark.anyio
async def test_create_lot_authorized(
    async_client: AsyncClient, auth_headers_admin: dict[str, str]
):
    name = "TestLot"
    payload = ParkingLotIn(
        name=name,
        location="Rotterdam",
        address="Wijnhaven 103",
        capacity=20,
        reserved=0,
        tariff=5.0,
        daytariff=30.0,
        latitude=51.926517,
        longitude=4.462456,
    )
    resp = await async_client.post(
        "/parking_lots",
        json=payload.model_dump(mode="json"),
        headers=auth_headers_admin,
    )

    # Expect 201 (Created)
    assert resp.status_code == 201
    data = ParkingLotOut.model_validate(resp.json())
    assert data.name == name


@pytest.mark.anyio
async def test_create_lot_unauthorized(
    async_client: AsyncClient, auth_headers_user: dict[str, str]
):
    name = "TestLot"
    payload = ParkingLotIn(
        name=name,
        location="Rotterdam",
        address="Wijnhaven 103",
        capacity=20,
        reserved=0,
        tariff=5.0,
        daytariff=30.0,
        latitude=51.926517,
        longitude=4.462456,
    )
    resp = await async_client.post(
        "/parking_lots",
        json=payload.model_dump(mode="json"),
        headers=auth_headers_user,
    )

    # Expect 403 (Forbidden)
    assert resp.status_code == 403
