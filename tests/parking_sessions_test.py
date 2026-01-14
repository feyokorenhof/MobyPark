from httpx import AsyncClient
import pytest

from app.models.gate import Gate
from app.schemas.gate import GateDecision, GateDirection, GateEventIn

from datetime import datetime


@pytest.mark.anyio
async def test_create_parking_session(async_client: AsyncClient, gate_in_db: Gate):
    gate = gate_in_db
    payload = GateEventIn(
        gate_id=gate.id,
        parking_lot_id=gate.parking_lot_id,
        license_plate="abcdefg",
        direction=GateDirection.entry,
        timestamp=datetime.now(),
    )
    resp = await async_client.post(
        f"/gate/{gate.id}", json=payload.model_dump(mode="json")
    )

    assert resp.status_code == 201
    data = resp.json()
    assert data["gate_id"] == gate.id
    assert data["decision"] == GateDecision.open
