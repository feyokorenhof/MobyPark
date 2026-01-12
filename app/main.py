from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.core.config import settings
from app.routers import auth, parking_lots, reservations, discounts
from app.services.exceptions import (
    InvalidTimeRange,
    ReservationNotFound,
    ReservationOverlap,
)


app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
app.include_router(parking_lots.router, prefix="/parking_lots", tags=["parking_lots"])
app.include_router(discounts.router, prefix="/discounts", tags=["discounts"])


# Handle our exceptions
@app.exception_handler(ReservationOverlap)
async def reservation_overlap_handler(_, exc: ReservationOverlap):
    return JSONResponse(
        status_code=409,
        content={"detail": "Time slot overlaps an existing reservation"},
    )


@app.exception_handler(ReservationNotFound)
async def reservation_not_found_handler(_, exc: ReservationNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": "Reservation could not be found"},
    )


@app.exception_handler(InvalidTimeRange)
async def invalid_time_range_handler(_, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "end_time must be after start_time"},
    )
