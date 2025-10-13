from __future__ import annotations  # <-- lets us use bare string class names safely
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, Integer
from datetime import datetime
from app.db.base import Base, TimestampMixin
import enum

from app.models.user import User
from app.models.spot import Spot

# --- optional: help linters know these exist ---
if TYPE_CHECKING:
    from app.models.spot import Spot

# ---------------------------------------------------------------------


class ReservationStatus(str, enum.Enum):
    HOLD = "HOLD"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ParkingLot(Base, TimestampMixin):
    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False)

    # relationship to Spot
    spots: Mapped[list[Spot]] = relationship(back_populates="lot", passive_deletes=True)


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    spot_id: Mapped[int] = mapped_column(
        ForeignKey("spots.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus, name="reservation_status"),  # PostgreSQL ENUM
        nullable=False,
    )

    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Reverse pairs:
    spot: Mapped["Spot"] = relationship(
        back_populates="reservations",
        passive_deletes=True,
    )
    user: Mapped["User"] = relationship(
        back_populates="reservations",
        passive_deletes=True,
    )
