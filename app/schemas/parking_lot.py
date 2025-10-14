from pydantic import BaseModel


class ParkingLotIn(BaseModel):
    lot_id: int
    label: str
    kind: str


class ParkingLotOut(BaseModel):
    id: int
    lot_id: int
    label: str
    kind: str

    class Config:
        from_attributes = (
            True  # <-- important for model_validate(reservation) in router
        )
