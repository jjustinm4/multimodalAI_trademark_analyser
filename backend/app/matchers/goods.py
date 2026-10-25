"""Goods proximity: re-scores already-surfaced candidates by cosine similarity of goods embeddings."""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies as deps
from app.database import vec

QUERY = text(
    """
    SELECT id, 1 - (goods_embedding <=> CAST(:q AS vector)) AS similarity
    FROM marks
    WHERE id = ANY(CAST(:ids AS int[]))
    """
)


async def score(session: AsyncSession, goods_description: str, candidate_ids: list[int]) -> dict[int, float]:
    if not candidate_ids:
        return {}
    q = vec(await asyncio.to_thread(deps.embed_text, goods_description))
    rows = (await session.execute(QUERY, {"q": q, "ids": list(candidate_ids)})).all()
    return {r.id: max(0.0, float(r.similarity)) for r in rows}
