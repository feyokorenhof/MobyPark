from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.payment import Payment
from app.models.user import User
from app.schemas.payment import PaymentIn
from app.services.exceptions import (
    InvalidCredentials,
    PaymentNotFound,
)


async def retrieve_payment(
    db: AsyncSession, payment_id: int, current_user: User
) -> Payment:
    existing = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = existing.scalar_one_or_none()
    if payment is None:
        raise PaymentNotFound()

    if payment.user_id != current_user.id:
        raise InvalidCredentials()
    return payment


async def create_payment(
    db: AsyncSession, payload: PaymentIn, current_user: User
) -> Payment:
    new_payment = Payment()

    db.add(new_payment)
    await db.flush()  # get PK (new_payment.id)

    await db.commit()
    await db.refresh(new_payment)
    return new_payment
