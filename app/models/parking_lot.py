from __future__ import annotations  # <-- lets us use bare string class names safely
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from app.db.base import Base, TimestampMixin


# --- optional: help linters know these exist ---
if TYPE_CHECKING:
    from app.models.spot import (
        Spot,
    )  # circular-safe imports


class ParkingLot(Base, TimestampMixin):
    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)

    # relationship to Spot
    spots: Mapped[list[Spot]] = relationship(back_populates="lot", passive_deletes=True)
