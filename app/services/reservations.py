from datetime import timezone
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

from app.services.discounts import apply_discount
from app.services.discount_redemption import redeem_discount_code


async def retrieve_reservation(db: AsyncSession, reservation_id: int):
    existing = await db.execute(
        select(Reservation).where(Reservation.id == reservation_id)
    )
    reservation = existing.scalar_one_or_none()

    if reservation is None:
        raise ReservationNotFound()

    return reservation


async def create_reservation(db: AsyncSession, payload: ReservationIn) -> Reservation:
    # 1) Normalize datetimes (prefer timezone-aware UTC)
    start = payload.start_time
    end = payload.end_time

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
                ~((Reservation.end_time <= start) | (Reservation.start_time >= end)),
            )
        )
    )
    overlap = (await db.execute(overlap_q)).scalar()
    if overlap:
        raise ReservationOverlap()

    # NEW: apply discount server-side (keep dc so we can redeem it)
    original_cost = payload.cost
    final_cost, discount_amount, discount_code_id, dc = await apply_discount(
        db=db,
        original_cost=original_cost,
        discount_code_str=payload.discount_code,
    )

    # 4) Create + persist
    new_res = Reservation(
        start_time=start,
        end_time=end,
        user_id=payload.user_id,
        parking_lot_id=payload.parking_lot_id,
        vehicle_id=payload.vehicle_id,
        status=ReservationStatus.confirmed,
        # store discount results
        cost=final_cost,
        original_cost=original_cost,
        discount_amount=discount_amount,
        discount_code_id=discount_code_id,
    )

    db.add(new_res)
    await db.flush()  # get PK (new_res.id)

    # NEW: mark discount as used (redemption + uses_count) BEFORE commit
    if dc:
        await redeem_discount_code(
            db=db,
            dc=dc,
            user_id=payload.user_id,
            reservation_id=new_res.id,
        )

    await db.commit()
    await db.refresh(new_res)
    return new_res
