from typing import TYPE_CHECKING, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, DateTime, Integer, Float
from datetime import datetime
from app.db.base import Base, TimestampMixin
import enum
from app.models.payment import Payment

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.vehicle import Vehicle
    from app.models.parking_lot import ParkingLot


class ReservationStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    parking_lot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_lots.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus, name="reservation_status"),
        nullable=False,
        default=ReservationStatus.confirmed,
    )

    cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)

    # --- Relationships ---
    user: Mapped["User"] = relationship(
        back_populates="reservations", passive_deletes=True
    )
    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="reservations", passive_deletes=True
    )
    parking_lot: Mapped["ParkingLot"] = relationship(
        back_populates="reservations", passive_deletes=True
    )
    payment: Mapped[Optional["Payment"]] = relationship(
        back_populates="reservation", uselist=False
    )
