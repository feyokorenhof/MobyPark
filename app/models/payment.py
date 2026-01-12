from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Float, DateTime, ForeignKey, JSON, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.reservation import Reservation
    from app.models.parking_session import ParkingSession


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    reservation_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("reservations.id", ondelete="SET NULL"), index=True, nullable=True
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("parking_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    transaction: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    initiator: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),  # let DB set it
    )

    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    hash: Mapped[Optional[str]] = mapped_column(String(100))
    t_data: Mapped[Optional[dict]] = mapped_column(JSON)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="payments")
    reservation: Mapped[Optional["Reservation"]] = relationship(
        back_populates="payment"
    )
    # Sessions with this payment
    session: Mapped["ParkingSession"] = relationship(back_populates="payment")
