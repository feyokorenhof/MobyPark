from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

from app.models.user import User
from app.schemas.parking_session import ParkingSessionOut
from app.services.auth import get_current_user
from app.services.parking_sessions import (
    retrieve_parking_session,
)


router = APIRouter()


@router.get(
    "/{parking_session_id}",
    response_model=ParkingSessionOut,
    status_code=status.HTTP_200_OK,
)
async def get_parking_session(
    parking_session_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    session = await retrieve_parking_session(db, parking_session_id)
    return ParkingSessionOut.model_validate(session)
