from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth
from app.routers import reservations


app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(reservations.router, prefix="/reservations", tags=["reservations"])
