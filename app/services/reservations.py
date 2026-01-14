from datetime import timezone
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, exists, select
from app.models.reservation import ReservationStatus
from app.schemas.reservations import ReservationIn
from app.models import Reservation
from app.services.exceptions import (
    InvalidTimeRange,
    ReservationNotFound,
    ReservationOverlap,
)


async def retrieve_reservation(db: AsyncSession, reservation_id: int):
    existing = await db.execute(
        select(Reservation).where(Reservation.id == reservation_id)
    )
    reservation = existing.scalar_one_or_none()

    if reservation is None:
        raise ReservationNotFound()


async def create_reservation(db: AsyncSession, payload: ReservationIn) -> Reservation:
    # 1) Normalize datetimes (prefer timezone-aware UTC)
    start = payload.planned_start
    end = payload.planned_end

    # If naive, assume UTC (adjust to your needs)
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    # 2) Basic validation
    if end <= start:
        raise InvalidTimeRange()

    # 3) (Optional) Prevent overlaps on the same parking spot
    # Overlap condition: NOT (existing.end <= start OR existing.start >= end)
    overlap_q = select(
        exists().where(
            and_(
                Reservation.parking_lot_id == payload.parking_lot_id,
                ~(
                    (Reservation.planned_end <= start)
                    | (Reservation.planned_start >= end)
                ),
            )
        )
    )
    overlap = (await db.execute(overlap_q)).scalar()
    if overlap:
        raise ReservationOverlap()

    # 4) Create + persist
    new_res = Reservation(
        planned_start=start,
        planned_end=end,
        user_id=payload.user_id,
        parking_lot_id=payload.parking_lot_id,
        vehicle_id=payload.vehicle_id,
        license_plate=payload.license_plate,
        status=ReservationStatus.confirmed,
        quoted_cost=20.0,
    )
    db.add(new_res)
    await db.flush()  # get PK
    await db.commit()
    await db.refresh(new_res)
    return new_res


async def try_get_valid_reservation_by_plate(
    db: AsyncSession, lot_id: int, plate: str, now: datetime
) -> Optional[Reservation]:
    q = select(Reservation).where(
        Reservation.parking_lot_id == lot_id,
        Reservation.license_plate == plate,
        Reservation.status == ReservationStatus.confirmed,
        Reservation.planned_start <= now,
        Reservation.planned_end >= now,
    )
    res = await db.execute(q)
    return res.scalar_one_or_none()
