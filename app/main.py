from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth, parking_lots, reservations


app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
app.include_router(parking_lots.router, prefix="/parking_lots", tags=["parking_lots"])
