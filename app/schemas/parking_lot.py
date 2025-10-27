from pydantic import BaseModel


class ParkingLotIn(BaseModel):
    name: str
    timezone: str


class ParkingLotOut(BaseModel):
    id: int
    name: str
    timezone: str

    class Config:
        from_attributes = (
            True  # <-- important for model_validate(reservation) in router
        )
