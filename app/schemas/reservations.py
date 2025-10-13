from enum import Enum
from pydantic import BaseModel
from datetime import datetime


# Mirror your SQLA Enum so input can be validated
class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class ReservationIn(BaseModel):
    starts_at: datetime
    ends_at: datetime
    user_id: int
    spot_id: int


class ReservationOut(BaseModel):
    id: int
    starts_at: datetime
    ends_at: datetime
    user_id: int
    spot_id: int
    status: ReservationStatus = ReservationStatus.pending

    class Config:
        from_attributes = (
            True  # <-- important for model_validate(reservation) in router
        )
