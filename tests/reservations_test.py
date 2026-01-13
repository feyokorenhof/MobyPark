from httpx import AsyncClient
import pytest

from app.models.parking_lot import ParkingLot
from app.models.reservation import ReservationStatus
from app.models.user import User
from app.models.vehicle import Vehicle


@pytest.mark.anyio
async def test_create_reservation(
    async_client: AsyncClient,
    user_in_db: User,
    lot_in_db: ParkingLot,
    vehicle_in_db: Vehicle,
):
    resp = await async_client.post(
        "/reservations",
        json={
            "planned_start": "2025-11-17 11:27:42.402",
            "planned_end": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
            "vehicle_id": vehicle_in_db.id,
            "status": ReservationStatus.pending,
            "quoted_cost": 20.0,
        },
    )

    # Expect 201 (Created) as no overlap should be happening
    assert resp.status_code == 201


@pytest.mark.anyio
async def test_create_reservation_overlap(
    async_client: AsyncClient,
    user_in_db: User,
    lot_in_db: ParkingLot,
    vehicle_in_db: Vehicle,
):
    resp1 = await async_client.post(
        "/reservations",
        json={
            "planned_start": "2025-11-17 11:27:42.402",
            "planned_end": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
            "vehicle_id": vehicle_in_db.id,
            "status": ReservationStatus.pending,
        },
    )
    # Expect 201 (Created)
    assert resp1.status_code == 201

    resp2 = await async_client.post(
        "/reservations",
        json={
            "planned_start": "2025-11-17 11:27:42.402",
            "planned_end": "2025-11-17 12:27:42.402",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
            "vehicle_id": vehicle_in_db.id,
            "status": ReservationStatus.pending,
        },
    )
    # Expect 409 (Conflict) because of overlapping times
    assert resp2.status_code == 409
