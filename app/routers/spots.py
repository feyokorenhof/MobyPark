from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.spot import Spot

from app.schemas.spot import SpotIn, SpotOut


router = APIRouter()


@router.get(
    "/{spot_id}",
    response_model=SpotOut,
    status_code=status.HTTP_200_OK,
)
async def get_spot(spot_id: int, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(select(Spot).where(Spot.id == spot_id))
    spot = existing.scalar_one_or_none()

    if spot is None:
        raise HTTPException(status_code=404, detail="Spot Not Found!")

    return SpotOut.model_validate(spot)


@router.post("", response_model=SpotOut, status_code=status.HTTP_201_CREATED)
async def add_spot(payload: SpotIn, db: AsyncSession = Depends(get_session)):
    # Create + persist

    new_spot = Spot(lot_id=payload.lot_id, label=payload.label, kind=payload.kind)

    db.add(new_spot)
    await db.flush()  # get PK
    await db.commit()
    await db.refresh(new_spot)

    return SpotOut.model_validate(new_spot)
