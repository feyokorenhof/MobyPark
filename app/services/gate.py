from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.gate import GateDecision, GateEventIn, GateEventOut

from app.services.parking_sessions import (
    close_session,
    create_session_anonymously,
    create_session_from_reservation,
    try_get_active_session_by_plate,
)
from app.services.reservations import try_get_valid_reservation_by_plate

from datetime import datetime


async def handle_gate_event(db: AsyncSession, payload: GateEventIn):
    # Check if reservation exists with license plate
    valid_reservation = await try_get_valid_reservation_by_plate(
        db, payload.parking_lot_id, payload.license_plate, datetime.now()
    )

    # Check if session exists with license plate
    active_session = await try_get_active_session_by_plate(
        db, payload.parking_lot_id, payload.license_plate
    )
    if payload.direction == "entry":
        # If there's already an active session, this is a duplicate entry hit
        if active_session is not None:
            return GateEventOut(
                gate_id=payload.gate_id,
                decision=GateDecision.deny,
                reason="session_already_active",
                session_id=active_session.id,
            )

        # If a valid reservation exists, start a session linked to it
        if valid_reservation:
            new_session = await create_session_from_reservation(
                db, valid_reservation, payload
            )
            return GateEventOut(
                gate_id=payload.gate_id,
                decision=GateDecision.open,
                reason="reservation_valid",
                session_id=new_session.id,
                reservation_id=valid_reservation.id,
            )

        # No reservation -> treat as anonymous drive-up if allowed
        session = await create_session_anonymously(db, payload)
        return GateEventOut(
            gate_id=payload.gate_id,
            decision=GateDecision.open,
            reason="anonymous_driveup_started",
            session_id=session.id,
        )

    if payload.direction == "exit":
        # To exit you typically must have an active session
        if not active_session:
            # TODO: ask PO if we let people out if they didn't have session
            # just log the anomaly
            return GateEventOut(
                gate_id=payload.gate_id,
                decision=GateDecision.open,
                reason="no_active_session",
            )

        await close_session(db, active_session, payload)
        return GateEventOut(
            gate_id=payload.gate_id,
            decision=GateDecision.open,
            reason="session_closed",
            session_id=active_session.id,
        )

    return GateEventOut(
        gate_id=payload.gate_id, decision=GateDecision.deny, reason="invalid_direction"
    )
