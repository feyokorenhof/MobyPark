from __future__ import annotations  # <-- lets us use bare string class names safely
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from app.db.base import Base, TimestampMixin


# --- optional: help linters know these exist ---
if TYPE_CHECKING:
    from app.models.reservation import (
        ParkingLot,
        Reservation,
    )  # circular-safe imports


class Spot(Base, TimestampMixin):
    __tablename__ = "spots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_lots.id", ondelete="CASCADE"), index=True, nullable=False
    )
    label: Mapped[str] = mapped_column(String(32), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), default="STANDARD", nullable=False)

    lot: Mapped[ParkingLot] = relationship(back_populates="spots")

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="spot",
        passive_deletes=True,  # DB handles ON DELETE CASCADE
    )
