from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.gate import GateEventIn, GateEventOut
from app.services.gate import handle_gate_event


router = APIRouter()


@router.post(
    "/{gate_id}", response_model=GateEventOut, status_code=status.HTTP_201_CREATED
)
async def on_gate_event(
    gate_id: int, payload: GateEventIn, db: AsyncSession = Depends(get_session)
):
    print(payload)
    return await handle_gate_event(db, payload)
