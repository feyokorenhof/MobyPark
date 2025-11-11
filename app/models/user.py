from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime
from app.db.base import Base, TimestampMixin
from datetime import datetime
from app.models.vehicle import Vehicle
from app.models.payment import Payment

# --- help linters : circular-safe imports ---
if TYPE_CHECKING:
    from app.models.reservation import Reservation


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    phone: Mapped[str] = mapped_column(String(15))
    role: Mapped[str] = mapped_column(String(15))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    birth_year: Mapped[int] = mapped_column()

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="user",
        passive_deletes=True,
    )
    vehicles: Mapped[list["Vehicle"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    payments: Mapped[list["Payment"]] = relationship(back_populates="user", cascade="all, delete-orphan")
