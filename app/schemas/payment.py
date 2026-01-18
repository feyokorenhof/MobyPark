from enum import Enum
from pydantic import BaseModel, ConfigDict


# Mirror SQLA Enum so input can be validated
class PaymentStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class PaymentIn(BaseModel):
    id: int


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: PaymentStatus
