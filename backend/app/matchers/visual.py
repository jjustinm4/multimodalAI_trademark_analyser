"""Visual matcher: CLIP ViT-B/32 image embedding, cosine search over logo embeddings."""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies as deps
from app.database import vec

QUERY = text(
    """
    SELECT id, mark_text, 1 - (logo_embedding <=> CAST(:q AS vector)) AS similarity
    FROM marks
    WHERE logo_embedding IS NOT NULL
    ORDER BY logo_embedding <=> CAST(:q AS vector)
    LIMIT :limit
    """
)


def _embed_logo(logo_b64: str):
    image = deps.decode_logo(logo_b64)
    return deps.embed_images([image])[0]


async def match(session: AsyncSession, logo_b64: str | None, limit: int = 100) -> list[dict]:
    if not logo_b64:
        return []
    q = vec(await asyncio.to_thread(_embed_logo, logo_b64))
    rows = (await session.execute(QUERY, {"q": q, "limit": limit})).all()
    return [{"id": r.id, "mark_text": r.mark_text, "score": max(0.0, float(r.similarity))} for r in rows]
