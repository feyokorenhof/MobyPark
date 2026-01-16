from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException

from app.models.discount_code import DiscountCode


async def get_discount_by_code(db: AsyncSession, code: str) -> DiscountCode:
    # case-insensitive match
    res = await db.execute(
        select(DiscountCode).where(func.lower(DiscountCode.code) == code.lower())
    )
    dc = res.scalar_one_or_none()
    if not dc:
        raise HTTPException(status_code=404, detail="Discount code not found")
    return dc


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


async def validate_discount_code(db: AsyncSession, dc: DiscountCode) -> None:
    now = _now_utc()

    if not dc.enabled:
        raise HTTPException(status_code=400, detail="Discount code is disabled")

    if dc.valid_from and now < dc.valid_from:
        raise HTTPException(status_code=400, detail="Discount code not active yet")

    if dc.valid_until and now > dc.valid_until:
        raise HTTPException(status_code=400, detail="Discount code expired")

    # single_use means only 1 redemption globally
    if dc.single_use and dc.uses_count >= 1:
        raise HTTPException(status_code=400, detail="Discount code already used")

    # max_uses (global) if set
    if dc.max_uses is not None and dc.uses_count >= dc.max_uses:
        raise HTTPException(status_code=400, detail="Discount code usage limit reached")

    # simple range validation
    if dc.percent < 0 or dc.percent > 100:
        raise HTTPException(status_code=400, detail="Invalid discount percent")


def calculate_discount(original_cost: float, percent: int) -> float:
    if original_cost <= 0:
        return 0.0
    amount = original_cost * (percent / 100.0)
    return round(amount, 2)


async def apply_discount(
    db: AsyncSession,
    original_cost: float,
    discount_code_str: str | None,
):
    """
    Returns: (final_cost, discount_amount, discount_code_id, discount_obj_or_none)
    """
    if not discount_code_str:
        return original_cost, 0.0, None, None

    dc = await get_discount_by_code(db, discount_code_str)
    await validate_discount_code(db, dc)

    discount_amount = calculate_discount(original_cost, dc.percent)
    final_cost = max(0.0, round(original_cost - discount_amount, 2))

    return final_cost, discount_amount, dc.id, dc
