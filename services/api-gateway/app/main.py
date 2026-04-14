from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.chat import router as chat_router
from app.routers.meals import router as meals_router
from app.routers.profile import router as profile_router
from app.routers.progress import router as progress_router
import app.models  # noqa: F401

app = FastAPI(title="Calorie AI Gateway", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(meals_router)
app.include_router(profile_router)
app.include_router(progress_router)
