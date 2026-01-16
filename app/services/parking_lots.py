from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.parking_lot import ParkingLot
from app.schemas.parking_lot import ParkingLotCostIn, ParkingLotIn
from app.services.exceptions import ParkingLotNotFound


async def retrieve_parking_lot(db: AsyncSession, parking_lot_id: int):
    existing = await db.execute(
        select(ParkingLot).where(ParkingLot.id == parking_lot_id)
    )
    parking_lot = existing.scalar_one_or_none()

    if parking_lot is None:
        raise ParkingLotNotFound()
    return parking_lot


async def create_parking_lot(db: AsyncSession, payload: ParkingLotIn):
    # Create + persist
    new_parking_lot = ParkingLot(
        name=payload.name,
        location=payload.location,
        address=payload.address,
        capacity=payload.capacity,
        reserved=payload.reserved,
        tariff=payload.tariff,
        daytariff=payload.daytariff,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )

    db.add(new_parking_lot)
    await db.flush()  # get PK
    await db.commit()
    await db.refresh(new_parking_lot)
    return new_parking_lot


async def get_parking_lot_cost(db: AsyncSession, payload: ParkingLotCostIn) -> float:
    existing = await db.execute(select(ParkingLot).where(ParkingLot.id == payload.id))
    parking_lot = existing.scalar_one_or_none()
    if parking_lot is None:
        raise ParkingLotNotFound()
    return (
        parking_lot.daytariff
        if payload.hours >= 6
        else parking_lot.tariff * payload.hours
    )
