from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# Mirror your SQLA Enum so input can be validated
class ReservationStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class ReservationIn(BaseModel):
    user_id: int
    parking_lot_id: int
    vehicle_id: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus
    cost: float
    discount_code: Optional[str] = None


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    parking_lot_id: int
    vehicle_id: int
    start_time: datetime
    end_time: datetime
    status: ReservationStatus
    cost: float
    original_cost: float
    discount_amount: float
    discount_code_id: Optional[int] = None
