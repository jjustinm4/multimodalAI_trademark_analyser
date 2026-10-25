"""GET /api/health — DB and LLM connectivity."""
import httpx
from fastapi import APIRouter
from sqlalchemy import text

from app.config import settings
from app.database import engine

router = APIRouter()


@router.get("/health")
async def health():
    db = "ok"
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        db = "unreachable"

    llm = "ok"
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(f"{settings.llm_base_url.rstrip('/')}/models")
            r.raise_for_status()
    except Exception:  # noqa: BLE001
        llm = "unreachable"

    return {"status": "ok", "llm": llm, "db": db}
