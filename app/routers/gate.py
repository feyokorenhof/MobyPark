from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.gate import GateEventIn, GateEventOut


router = APIRouter()


@router.post("", response_model=GateEventOut, status_code=status.HTTP_201_CREATED)
async def handle_gate_event(
    payload: GateEventIn, db: AsyncSession = Depends(get_session)
):
    pass
