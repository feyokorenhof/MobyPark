from enum import Enum
from pydantic import BaseModel, ConfigDict
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
    parking_lot_id: int


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    starts_at: datetime
    ends_at: datetime
    user_id: int
    parking_lot_id: int
    status: ReservationStatus = ReservationStatus.pending
