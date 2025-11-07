from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginIn, LoginOut, RegisterIn, RegisterOut, UserOut
from app.services.security import hash_password, verify_password, needs_update
from datetime import datetime, timezone, timedelta
import jwt

import os


router = APIRouter()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "30"))

# A precomputed dummy hash to equalize timing on nonexistent users.
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$J3y9q7dF9J2mP7c9bZ2xVA$C3Xj2mD5ZQBM3pqT+o7+4w"  # example


def create_access_token(sub: str) -> str:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(minutes=JWT_EXP_MIN)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


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


@router.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_session)):
    # 1) fetch user by email
    res = await db.execute(select(User).where(User.email == payload.email))
    user: User | None = res.scalar_one_or_none()

    # 2) verify password (timing-safe pattern)
    if not user:
        # do a dummy verify to keep timing similar
        verify_password(payload.password, DUMMY_HASH)
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3) optional: upgrade hash transparently if policy changed
    if needs_update(user.password_hash):
        user.password_hash = hash_password(payload.password)
        await db.flush()
        await db.commit()

    # 4) issue JWT
    token = create_access_token(sub=str(user.id))
    return LoginOut(access_token=token, token_type="bearer")


@router.get("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def user(user_id: int, db: AsyncSession = Depends(get_session)):
    existing = await db.execute(select(User).where(User.id == user_id))
    user = existing.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserOut(id=user.id)
