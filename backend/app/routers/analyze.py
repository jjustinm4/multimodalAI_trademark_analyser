"""POST /api/analyze — the full examination pipeline."""
import asyncio
import time

from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from app import dependencies as deps
from app.classifier import nice
from app.database import SessionLocal
from app.drafter import report
from app.matchers import fusion, goods, phonetic, semantic, visual
from app.models import Mark
from app.rag import retrieval
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.screener import grounds

router = APIRouter()


async def _with_session(fn, *args):
    async with SessionLocal() as session:
        return await fn(session, *args)


async def _timed(timings: dict, name: str, coro):
    t0 = time.perf_counter()
    result = await coro
    timings[name] = round((time.perf_counter() - t0) * 1000, 1)
    return result


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    timings: dict[str, float] = {}
    t_start = time.perf_counter()

    use_visual = bool(req.logo_file)
    if use_visual:
        try:
            await asyncio.to_thread(deps.decode_logo, req.logo_file)
        except Exception as exc:  # noqa: BLE001
            raise HTTPException(400, "Could not read the logo image. Upload a PNG, JPG or SVG file.") from exc

    # Stage 1: independent matchers + classification in parallel (one DB session each).
    ph, se, vi, classes = await asyncio.gather(
        _timed(timings, "phonetic", _with_session(phonetic.match, req.mark_text)),
        _timed(timings, "semantic", _with_session(semantic.match, req.mark_text)),
        _timed(timings, "visual", _with_session(visual.match, req.logo_file)),
        _timed(timings, "classify", _with_session(nice.classify, req.goods_description)),
    )
    t0 = time.perf_counter()
    grounds_result = grounds.screen(req.mark_text)
    timings["grounds"] = round((time.perf_counter() - t0) * 1000, 1)

    # Stage 2: goods proximity re-scores the union of candidates, then fuse.
    candidate_ids = list({h["id"] for hits in (ph, se, vi) for h in hits})
    goods_scores = await _timed(timings, "goods", _with_session(goods.score, req.goods_description, candidate_ids))
    ranked, weights = fusion.fuse({"phonetic": ph, "semantic": se, "visual": vi}, goods_scores, use_visual)

    async with SessionLocal() as session:
        rows = (await session.execute(select(Mark).where(Mark.id.in_([r["id"] for r in ranked])))).scalars().all()
    by_id = {m.id: m for m in rows}
    full_scores = lambda d: {k: round(d.get(k, 0.0), 4) for k in fusion.MATCHERS}  # noqa: E731
    citations = []
    for r in ranked:
        m = by_id[r["id"]]
        citations.append({
            "id": m.id, "mark_text": m.mark_text, "nice_class": m.nice_class,
            "goods_description": m.goods_description, "status": m.status, "owner_name": m.owner_name,
            "logo_svg": m.logo_svg, "scores": full_scores(r["scores"]),
            "contributions": full_scores(r["contributions"]), "final_score": round(r["final_score"], 4),
        })

    provided = req.nice_class
    nice_result = {
        "top_classes": classes,
        "provided_class": provided,
        "matches_top": (classes[0]["class_number"] == provided) if (provided and classes) else None,
    }

    precedent = await _timed(timings, "precedent", _with_session(
        retrieval.retrieve, req.mark_text, citations[0]["mark_text"] if citations else None, req.goods_description))

    query = {
        "mark_text": req.mark_text,
        "goods_description": req.goods_description,
        "nice_class": provided or (classes[0]["class_number"] if classes else None),
        "nice_class_source": "provided" if provided else "suggested",
        "has_logo": use_visual,
    }
    drafted = await _timed(timings, "report", report.draft(query, citations, grounds_result, nice_result, precedent))
    timings["total"] = round((time.perf_counter() - t_start) * 1000, 1)

    return {
        "query": query,
        "weights": {k: round(v, 4) for k, v in weights.items()},
        "citations": citations,
        "nice_class": nice_result,
        "grounds": grounds_result,
        "precedent": precedent,
        "report": drafted["report"],
        "report_source": drafted["source"],
        "report_warning": drafted["warning"],
        "timings_ms": timings,
    }
