from httpx import AsyncClient
import pytest

from app.models.parking_lot import ParkingLot
from app.models.user import User


@pytest.mark.anyio
async def test_create_reservation(
    async_client: AsyncClient, user_in_db: User, lot_in_db: ParkingLot
):
    resp = await async_client.post(
        "/reservations",
        json={
            "starts_at": "2025-11-17 11:27:42.402",
            "ends_at": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
        },
    )

    # Expect 201 (Created) as no overlap should be happening
    assert resp.status_code == 201


@pytest.mark.anyio
async def test_create_reservation_overlap(
    async_client: AsyncClient, user_in_db: User, lot_in_db: ParkingLot
):
    resp1 = await async_client.post(
        "/reservations",
        json={
            "starts_at": "2025-11-17 11:27:42.402",
            "ends_at": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
        },
    )
    # Expect 201 (Created)
    assert resp1.status_code == 201

    resp2 = await async_client.post(
        "/reservations",
        json={
            "starts_at": "2025-11-17 11:27:42.402",
            "ends_at": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
        },
    )
    # Expect 409 (Conflict) because of overlapping times
    assert resp2.status_code == 409
