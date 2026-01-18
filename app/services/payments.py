from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.parking_session import ParkingSession, SessionStatus
from app.models.payment import Payment, PaymentStatus
from app.models.user import User
from app.schemas.payment import PaymentIn
from app.services.exceptions import (
    PaymentNotFound,
)


async def retrieve_payment(
    db: AsyncSession, payment_id: int, current_user: User
) -> Payment:
    existing = await db.execute(
        select(Payment)
        .where(Payment.id == payment_id)
        .options(selectinload(ParkingSession.payment))
    )
    payment = existing.scalar_one_or_none()
    if payment is None:
        raise PaymentNotFound()

    return payment


async def retrieve_payment_by_plate_and_parking_lot_id(
    db: AsyncSession, payment: PaymentIn, current_user: User
) -> Payment:
    existing = await db.execute(
        select(Payment)
        .join(Payment.session)
        .where(ParkingSession.parking_lot_id == payment.parking_lot_id)
        .where(ParkingSession.license_plate == payment.license_plate)
        .where(ParkingSession.status == SessionStatus.active)
        .options(selectinload(Payment.session))
    )

    existing_payment = existing.scalar_one_or_none()
    if existing_payment is None:
        raise PaymentNotFound()

    return existing_payment


async def create_payment(
    db: AsyncSession, payload: PaymentIn, current_user: User
) -> Payment:
    new_payment = Payment()

    db.add(new_payment)
    await db.flush()  # get PK (new_payment.id)

    await db.commit()
    await db.refresh(new_payment)
    return new_payment


async def mark_payment_paid(
    db: AsyncSession, payment: PaymentIn, user: User
) -> Payment:
    active_payment = await retrieve_payment_by_plate_and_parking_lot_id(
        db, payment, user
    )

    if active_payment.status == PaymentStatus.paid:
        return active_payment

    active_payment.status = PaymentStatus.paid
    active_payment.session.amount_paid = active_payment.session.amount_due

    await db.commit()
    await db.refresh(active_payment)
    return active_payment
