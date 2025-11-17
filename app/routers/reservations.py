from datetime import timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.reservation import ReservationStatus
from app.schemas.reservations import ReservationIn, ReservationOut
from app.models import Reservation
from sqlalchemy import and_, exists


router = APIRouter()


@router.get(
    "/{reservation_id}",
    response_model=ReservationOut,
    status_code=status.HTTP_200_OK,
)
async def get_reservation(reservation_id: int, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(
        select(Reservation).where(Reservation.id == reservation_id)
    )
    reservation = existing.scalar_one_or_none()

    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation Not Found!")

    return ReservationOut.model_validate(reservation)


@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def add_reservation(
    payload: ReservationIn, db: AsyncSession = Depends(get_session)
):
    # 1) Normalize datetimes (prefer timezone-aware UTC)
    start = payload.starts_at
    end = payload.ends_at

    # If naive, assume UTC (adjust to your needs)
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)

    # 2) Basic validation
    if end <= start:
        raise HTTPException(status_code=422, detail="end_time must be after start_time")

    # 3) (Optional) Prevent overlaps on the same parking spot
    # Overlap condition: NOT (existing.end <= start OR existing.start >= end)
    overlap_q = select(
        exists().where(
            and_(
                Reservation.parking_lot_id == payload.parking_lot_id,
                ~((Reservation.ends_at <= start) | (Reservation.starts_at >= end)),
            )
        )
    )
    overlap = (await db.execute(overlap_q)).scalar()
    if overlap:
        raise HTTPException(
            status_code=409, detail="Time slot overlaps an existing reservation"
        )

    # 4) Create + persist
    new_res = Reservation(
        starts_at=start,
        ends_at=end,
        user_id=payload.user_id,
        parking_lot_id=payload.parking_lot_id,
        status=ReservationStatus.confirmed,
    )
    db.add(new_res)
    await db.flush()  # get PK
    await db.commit()
    await db.refresh(new_res)

    return ReservationOut.model_validate(new_res)
