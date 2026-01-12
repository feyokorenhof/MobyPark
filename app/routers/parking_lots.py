from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

from app.schemas.parking_lot import ParkingLotIn, ParkingLotOut
from app.services.parking_lots import create_parking_lot, retrieve_parking_lot


router = APIRouter()


@router.get(
    "/{parking_lot_id}",
    response_model=ParkingLotOut,
    status_code=status.HTTP_200_OK,
)
async def get_parking_lot(parking_lot_id: int, db: AsyncSession = Depends(get_session)):
    parking_lot = retrieve_parking_lot(db, parking_lot_id)
    return ParkingLotOut.model_validate(parking_lot)


@router.post("", response_model=ParkingLotOut, status_code=status.HTTP_201_CREATED)
async def add_parking_lot(
    payload: ParkingLotIn, db: AsyncSession = Depends(get_session)
):
    new_parking_lot = create_parking_lot(db, payload)
    return ParkingLotOut.model_validate(new_parking_lot)
