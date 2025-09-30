from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Enum, DateTime, Integer
from app.db.base import Base, TimestampMixin
import enum


class ReservationStatus(str, enum.Enum):
    HOLD = "HOLD"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"


class ParkingLot(Base, TimestampMixin):
    __tablename__ = "parking_lots"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    timezone: Mapped[str] = mapped_column(String(64))


class Spot(Base, TimestampMixin):
    __tablename__ = "spots"
    id: Mapped[int] = mapped_column(primary_key=True)
    lot_id: Mapped[int] = mapped_column(
        ForeignKey("parking_lots.id", ondelete="CASCADE"), index=True
    )
    label: Mapped[str] = mapped_column(String(32))
    kind: Mapped[str] = mapped_column(String(32), default="STANDARD")


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"
