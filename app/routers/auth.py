from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.models.user import User
from app.schemas.auth import LoginIn, LoginOut, RegisterIn, RegisterOut, UserOut
from app.services.auth import (
    create_user,
    create_admin,
    get_user,
    login_account,
    require_roles,
)


router = APIRouter()


@router.post(
    "/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_session)):
    user = await create_user(db, payload)
    return RegisterOut(id=user.id, email=user.email, name=user.name)


@router.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_session)):
    return await login_account(db, payload)


@router.get("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await get_user(db, user_id)


@router.post(
    "/register_admin",
    response_model=RegisterOut,
    status_code=status.HTTP_201_CREATED,
)
async def register_admin(
    payload: RegisterIn,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_roles("admin")),
):
    admin = await create_admin(db, payload)
    return RegisterOut(id=admin.id, email=admin.email, name=admin.name)
