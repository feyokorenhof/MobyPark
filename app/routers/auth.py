from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.auth import LoginIn, LoginOut, RegisterIn, RegisterOut, UserOut
from app.services.auth import create_account, get_user, login_account


router = APIRouter()


@router.post(
    "/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED
)
async def register(payload: RegisterIn, db: AsyncSession = Depends(get_session)):
    user = await create_account(db, payload)
    return RegisterOut(id=user.id, email=user.email, name=user.name)


@router.post("/login", response_model=LoginOut, status_code=status.HTTP_200_OK)
async def login(payload: LoginIn, db: AsyncSession = Depends(get_session)):
    return await login_account(db, payload)


@router.get("/users/{user_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def user(user_id: int, db: AsyncSession = Depends(get_session)):
    return await get_user(db, user_id)
