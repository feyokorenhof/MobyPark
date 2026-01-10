from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.reservations import ReservationIn, ReservationOut
from app.services.exceptions import (
    InvalidTimeRange,
    ReservationNotFound,
    ReservationOverlap,
)
from app.services.reservations import create_reservation, retrieve_reservation


router = APIRouter()


@router.get(
    "/{reservation_id}",
    response_model=ReservationOut,
    status_code=status.HTTP_200_OK,
)
async def get_reservation(reservation_id: int, db: AsyncSession = Depends(get_session)):
    try:
        reservation = await retrieve_reservation(db, reservation_id)
    except ReservationNotFound:
        raise HTTPException(status_code=404, detail="Reservation Not Found!")

    return ReservationOut.model_validate(reservation)


@router.post("", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def add_reservation(
    payload: ReservationIn, db: AsyncSession = Depends(get_session)
):
    try:
        # app.services.reservation.py
        new_res = await create_reservation(db, payload)
    except InvalidTimeRange:
        raise HTTPException(status_code=422, detail="end_time must be after start_time")
    except ReservationOverlap:
        raise HTTPException(
            status_code=409, detail="Time slot overlaps an existing reservation"
        )
    return ReservationOut.model_validate(new_res)
