from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import RegisterIn, RegisterOut
from app.services.security import hash_password


router = APIRouter()


@router.post(
    "/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(
        email=payload.email,
        name=payload.name,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return RegisterOut(id=user.id, email=user.email, name=user.name)
