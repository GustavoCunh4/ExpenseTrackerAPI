from fastapi import FastAPI

from app.api.v1.auth.router import router as auth_router
from app.api.v1.categories.router import router as categories_router
from app.api.v1.expenses.router import router as expenses_router
from app.core.config import get_settings
from app.core.db import init_db

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(expenses_router, prefix="/api/v1/expenses", tags=["expenses"])
