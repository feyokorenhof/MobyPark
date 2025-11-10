from httpx import AsyncClient
import pytest

from app.models.parking_lot import ParkingLot
from app.models.user import User


@pytest.mark.anyio
async def test_create_reservation(
    async_client: AsyncClient, user_in_db: User, lot_in_db: ParkingLot
):
    resp = await async_client.post(
        "/reservations/",
        json={
            "starts_at": "",
            "ends_at": "",
            "user_id": user_in_db.id,
            "parking_lot_id": lot_in_db.id,
        },
    )

    # Created or Overlaps existing reservation are both valid
    assert resp.status_code == 201 or resp.status_code == 409
