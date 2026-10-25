"""Semantic matcher: all-MiniLM-L6-v2 embedding of the mark text, cosine search over pgvector."""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies as deps
from app.database import vec

QUERY = text(
    """
    SELECT id, mark_text, 1 - (text_embedding <=> CAST(:q AS vector)) AS similarity
    FROM marks
    ORDER BY text_embedding <=> CAST(:q AS vector)
    LIMIT :limit
    """
)


async def match(session: AsyncSession, mark_text: str, limit: int = 100) -> list[dict]:
    q = vec(await asyncio.to_thread(deps.embed_text, mark_text))
    rows = (await session.execute(QUERY, {"q": q, "limit": limit})).all()
    return [{"id": r.id, "mark_text": r.mark_text, "score": max(0.0, float(r.similarity))} for r in rows]
