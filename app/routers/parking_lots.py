from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.parking_lot import ParkingLot

from app.schemas.parking_lot import ParkingLotIn, ParkingLotOut


router = APIRouter()


@router.get(
    "/{parking_lot_id}",
    response_model=ParkingLotOut,
    status_code=status.HTTP_200_OK,
)
async def get_parking_lot(parking_lot_id: int, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(
        select(ParkingLot).where(ParkingLot.id == parking_lot_id)
    )
    parking_lot = existing.scalar_one_or_none()

    if parking_lot is None:
        raise HTTPException(status_code=404, detail="Parking Lot Not Found!")

    return ParkingLotOut.model_validate(parking_lot)


@router.post("", response_model=ParkingLotOut, status_code=status.HTTP_201_CREATED)
async def add_parking_lot(
    payload: ParkingLotIn, db: AsyncSession = Depends(get_session)
):
    # Create + persist

    new_parking_lot = ParkingLot(name=payload.name, timezone=payload.timezone)

    db.add(new_parking_lot)
    await db.flush()  # get PK
    await db.commit()
    await db.refresh(new_parking_lot)

    return ParkingLotOut.model_validate(new_parking_lot)
