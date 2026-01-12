from datetime import datetime, timedelta, timezone
import os
import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import LoginIn, LoginOut, RegisterIn, UserOut
from app.services.exceptions import (
    AccountAlreadyExists,
    InvalidCredentials,
    UserNotFound,
)
from app.services.security import hash_password, needs_update, verify_password

JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
JWT_EXP_MIN = int(os.getenv("JWT_EXP_MIN", "30"))

# A precomputed dummy hash to equalize timing on nonexistent users.
DUMMY_HASH = (
    "$argon2id$v=19$m=65536,t=3,p=4$J3y9q7dF9J2mP7c9bZ2xVA$C3Xj2mD5ZQBM3pqT+o7+4w"
)


def create_access_token(sub: str) -> str:
    now = datetime.now(tz=timezone.utc)
    exp = now + timedelta(minutes=JWT_EXP_MIN)
    payload = {"sub": sub, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


async def create_account(db: AsyncSession, payload: RegisterIn):
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise AccountAlreadyExists()

    user = User(
        email=payload.email,
        name=payload.name,
        username=payload.username,
        phone=payload.phone,
        role=payload.role,
        active=payload.active,
        birth_year=payload.birth_year,
        password_hash=hash_password(payload.password),
    )

    db.add(user)
    await db.flush()
    await db.commit()
    await db.refresh(user)
    return user


async def login_account(db: AsyncSession, payload: LoginIn):
    # 1) fetch user by email
    res = await db.execute(select(User).where(User.email == payload.email))
    user: User | None = res.scalar_one_or_none()

    # 2) verify password (timing-safe pattern)
    if not user:
        # do a dummy verify to keep timing similar
        verify_password(payload.password, DUMMY_HASH)
        raise InvalidCredentials()

    if not verify_password(payload.password, user.password_hash):
        raise InvalidCredentials()

    # 3) optional: upgrade hash transparently if policy changed
    if needs_update(user.password_hash):
        user.password_hash = hash_password(payload.password)
        await db.flush()
        await db.commit()

    # 4) issue JWT
    token = create_access_token(sub=str(user.id))
    return LoginOut(access_token=token, token_type="bearer")


async def get_user(db: AsyncSession, user_id: int):
    existing = await db.execute(select(User).where(User.id == user_id))
    user = existing.scalar_one_or_none()
    if not user:
        raise UserNotFound()

    return UserOut(id=user.id)
