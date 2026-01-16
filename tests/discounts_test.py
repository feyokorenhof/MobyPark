"""
tests/discounts_test.py

Pure unit tests for the discount service.

"""

from __future__ import annotations

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

from app.models.discount_code import DiscountCode
from app.services import discounts


# --------------------------
# Helpers
# --------------------------


def make_discount(
    code="WELCOME20",
    percent=20,
    enabled=True,
    uses_count=0,
):
    return DiscountCode(
        id=1,
        code=code,
        percent=percent,
        enabled=enabled,
        single_use=False,
        max_uses=None,
        uses_count=uses_count,
        valid_from=None,
        valid_until=None,
    )


# --------------------------
# calculate_discount
# --------------------------


@pytest.mark.anyio
async def test_calculate_discount_basic():
    assert discounts.calculate_discount(100.0, 20) == 20.0


@pytest.mark.anyio
async def test_calculate_discount_zero_or_negative():
    assert discounts.calculate_discount(0.0, 20) == 0.0
    assert discounts.calculate_discount(-10.0, 20) == 0.0


# --------------------------
# apply_discount (mocked DB)
# --------------------------


@pytest.mark.anyio
async def test_apply_discount_no_code():
    final_cost, discount_amount, code_id, dc = await discounts.apply_discount(
        db=AsyncMock(spec=AsyncSession),
        original_cost=50.0,
        discount_code_str=None,
    )

    assert final_cost == 50.0
    assert discount_amount == 0.0
    assert code_id is None
    assert dc is None


@pytest.mark.anyio
async def test_apply_discount_valid_code(monkeypatch):
    fake_discount = make_discount()

    # Mock DB lookup
    monkeypatch.setattr(
        discounts,
        "get_discount_by_code",
        AsyncMock(return_value=fake_discount),
    )

    # Validation should pass
    monkeypatch.setattr(
        discounts,
        "validate_discount_code",
        AsyncMock(return_value=None),
    )

    final_cost, discount_amount, code_id, dc = await discounts.apply_discount(
        db=AsyncMock(spec=AsyncSession),
        original_cost=100.0,
        discount_code_str="WELCOME20",
    )

    assert discount_amount == 20.0
    assert final_cost == 80.0
    assert code_id == 1
    assert dc.code == "WELCOME20"
