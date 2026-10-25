"""Nice classifier: nearest-neighbour of the goods embedding against the 69 class reference entries."""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies as deps
from app.database import vec

QUERY = text(
    """
    SELECT class_number, class_name, 1 - (embedding <=> CAST(:q AS vector)) AS similarity
    FROM nice_classes
    ORDER BY embedding <=> CAST(:q AS vector)
    LIMIT 20
    """
)


async def classify(session: AsyncSession, goods_description: str, top_k: int = 3) -> list[dict]:
    q = vec(await asyncio.to_thread(deps.embed_text, goods_description))
    rows = (await session.execute(QUERY, {"q": q})).all()
    # Several reference entries can share a class; keep each class's best entry.
    best: dict[int, dict] = {}
    for r in rows:
        if r.class_number not in best:
            best[r.class_number] = {
                "class_number": r.class_number,
                "class_name": r.class_name,
                "confidence": round(max(0.0, float(r.similarity)), 4),
            }
    return list(best.values())[:top_k]
