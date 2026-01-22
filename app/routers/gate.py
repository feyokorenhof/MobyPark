from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.schemas.gate import GateEventIn, GateEventOut, GateIn, GateOut
from app.services.auth import require_roles
from app.services.gate import create_gate, delete_gate, handle_gate_event, update_gate


router = APIRouter()


@router.post("/{gate_id}", response_model=GateEventOut, status_code=status.HTTP_200_OK)
async def on_gate_event(
    gate_id: int, payload: GateEventIn, db: AsyncSession = Depends(get_session)
):
    return await handle_gate_event(db, payload)


@router.post("", response_model=GateOut, status_code=status.HTTP_201_CREATED)
async def add_gate(
    payload: GateIn,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles("admin")),
):
    new_gate = await create_gate(db, payload)
    return GateOut(id=new_gate.id, parking_lot_id=new_gate.parking_lot_id)


@router.put("/{gate_id}", response_model=GateOut, status_code=status.HTTP_200_OK)
async def edit_gate(
    gate_id: int,
    payload: GateIn,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles("admin")),
):
    # app.services.gate.py
    updated_gate = await update_gate(db, gate_id, payload)
    return GateOut(id=updated_gate.id, parking_lot_id=updated_gate.parking_lot_id)


@router.delete("/{gate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_gate(
    gate_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles("admin")),
):
    # app.services.gate.py
    await delete_gate(db, gate_id)
