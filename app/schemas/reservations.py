from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


# Mirror SQLA Enum so input can be validated
class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class ReservationIn(BaseModel):
    user_id: int
    parking_lot_id: int
    vehicle_id: int
    license_plate: str
    planned_start: datetime
    planned_end: datetime


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    parking_lot_id: int
    vehicle_id: int
    license_plate: str
    planned_start: datetime
    planned_end: datetime
    status: ReservationStatus
    quoted_cost: float
