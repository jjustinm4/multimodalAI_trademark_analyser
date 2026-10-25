"""GET /api/search — quick phonetic + semantic search, no report."""
import asyncio

from fastapi import APIRouter, Query
from sqlalchemy import select

from app.database import SessionLocal
from app.matchers import fusion, phonetic, semantic
from app.models import Mark
from app.schemas import SearchResponse

router = APIRouter()


async def _with_session(fn, *args):
    async with SessionLocal() as session:
        return await fn(session, *args)


@router.get("/search", response_model=SearchResponse)
async def search(q: str = Query(min_length=1, max_length=120), limit: int = Query(25, ge=1, le=100)):
    ph, se = await asyncio.gather(_with_session(phonetic.match, q), _with_session(semantic.match, q))
    ranked, _ = fusion.fuse({"phonetic": ph, "semantic": se}, None, use_visual=False, top_k=limit,
                            include=("phonetic", "semantic"))
    async with SessionLocal() as session:
        rows = (await session.execute(select(Mark).where(Mark.id.in_([r["id"] for r in ranked])))).scalars().all()
    by_id = {m.id: m for m in rows}
    return {"results": [
        {"id": r["id"], "mark_text": by_id[r["id"]].mark_text, "nice_class": by_id[r["id"]].nice_class,
         "goods": by_id[r["id"]].goods_description, "status": by_id[r["id"]].status,
         "similarity": round(r["final_score"], 4), "phonetic": round(r["scores"]["phonetic"], 4),
         "semantic": round(r["scores"]["semantic"], 4)}
        for r in ranked
    ]}
