from httpx import AsyncClient
import pytest

from app.models.gate import Gate
from app.schemas.gate import GateDecision, GateDirection, GateEventIn

from datetime import datetime


@pytest.mark.anyio
async def test_gate_entry(async_client: AsyncClient, gate_in_db: Gate):
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


@pytest.mark.anyio
async def test_gate_exit(async_client: AsyncClient, gate_in_db: Gate):
    # Entry
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

    # Exit
    payload_exit = GateEventIn(
        gate_id=gate.id,
        parking_lot_id=gate.parking_lot_id,
        license_plate="abcdefg",
        direction=GateDirection.exit,
        timestamp=datetime.now(),
    )

    resp_exit = await async_client.post(
        f"/gate/{gate.id}", json=payload_exit.model_dump(mode="json")
    )

    assert resp_exit.status_code == 201
    data_exit = resp_exit.json()
    assert data_exit["gate_id"] == gate.id
    assert data_exit["decision"] == GateDecision.open
