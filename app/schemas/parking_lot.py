from pydantic import BaseModel, ConfigDict


class ParkingLotIn(BaseModel):
    name: str
    timezone: str


class ParkingLotOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    timezone: str
