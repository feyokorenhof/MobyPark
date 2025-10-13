from __future__ import annotations  # <-- lets us use bare string class names safely
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, Integer
from datetime import datetime
from app.db.base import Base, TimestampMixin
import enum

# --- optional: help linters know these exist ---
if TYPE_CHECKING:
    from app.models.reservation import (
        Spot,
        ParkingLot,
        Reservation,
    )  # circular-safe imports
    # or if they were in separate modules:
    # from app.models.spot import Spot
    # from app.models.parking_lot import ParkingLot


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
    spots: Mapped[list[Spot]] = relationship(
        back_populates="lot", cascade="all, delete-orphan"
    )


class Spot(Base, TimestampMixin):
    __tablename__ = "spots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_lots.id", ondelete="CASCADE"), index=True, nullable=False
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), default="STANDARD", nullable=False)

    lot: Mapped[ParkingLot] = relationship(back_populates="spots")
    reservations: Mapped[list[Reservation]] = relationship(
        back_populates="spot", cascade="all, delete-orphan"
    )


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    spot_id: Mapped[int] = mapped_column(
        ForeignKey("spots.id", ondelete="CASCADE"), index=True, nullable=False
    )
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus, name="reservation_status"), nullable=False
    )
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    spot: Mapped[Spot] = relationship(back_populates="reservations")
