from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
import os

ROOT_DIR = Path(__file__).resolve().parents[4]
load_dotenv(ROOT_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
if DATABASE_URL.startswith("sqlite:///./"):
    DATABASE_URL = f"sqlite:///{ROOT_DIR / DATABASE_URL.replace('sqlite:///./', '')}"

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
