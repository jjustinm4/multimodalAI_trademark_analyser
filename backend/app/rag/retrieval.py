"""Precedent retrieval: embed the query context and fetch the nearest TTAB decision passages."""
import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app import dependencies as deps
from app.database import vec

QUERY = text(
    """
    SELECT proceeding_number, decision_date, mark_a, mark_b, outcome, text,
           1 - (embedding <=> CAST(:q AS vector)) AS similarity
    FROM precedent_chunks
    ORDER BY embedding <=> CAST(:q AS vector)
    LIMIT 12
    """
)


def build_query(mark_text: str, top_cited: str | None, goods_description: str) -> str:
    parts = [f"Likelihood of confusion between {mark_text.upper()}"]
    if top_cited:
        parts.append(f"and {top_cited.upper()}")
    parts.append(f"for {goods_description}")
    return " ".join(parts)


async def retrieve(session: AsyncSession, mark_text: str, top_cited: str | None, goods_description: str,
                   top_k: int = 3) -> list[dict]:
    q = vec(await asyncio.to_thread(deps.embed_text, build_query(mark_text, top_cited, goods_description)))
    rows = (await session.execute(QUERY, {"q": q})).all()
    out, seen = [], set()
    for r in rows:  # one passage per proceeding
        if r.proceeding_number in seen:
            continue
        seen.add(r.proceeding_number)
        out.append({
            "proceeding_number": r.proceeding_number,
            "decision_date": r.decision_date,
            "mark_a": r.mark_a,
            "mark_b": r.mark_b,
            "outcome": r.outcome,
            "excerpt": r.text,
            "similarity": round(float(r.similarity), 4),
        })
        if len(out) == top_k:
            break
    return out
