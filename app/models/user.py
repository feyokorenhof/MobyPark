from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from app.db.base import Base, TimestampMixin


# --- help linters : circular-safe imports ---
if TYPE_CHECKING:
    from app.models.reservation import Reservation


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    reservations: Mapped[list["Reservation"]] = relationship(
        back_populates="user",
        passive_deletes=True,
    )
