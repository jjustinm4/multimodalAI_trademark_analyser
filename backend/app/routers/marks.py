"""GET /api/marks and /api/marks/{id} — browse the synthetic corpus."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models import Mark
from app.schemas import MarkOut, MarkPage

router = APIRouter()

SORTS = {
    "id": Mark.id, "mark_text": Mark.mark_text, "nice_class": Mark.nice_class,
    "status": Mark.status, "filing_date": Mark.filing_date, "owner_name": Mark.owner_name,
}


def _out(m: Mark) -> dict:
    return {
        "id": m.id, "mark_text": m.mark_text, "nice_class": m.nice_class, "goods_description": m.goods_description,
        "status": m.status, "owner_name": m.owner_name, "filing_date": m.filing_date, "logo_svg": m.logo_svg,
        "phonetic_keys": m.phonetic_keys or [],
    }


@router.get("/marks", response_model=MarkPage)
async def list_marks(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    q: str | None = Query(None, max_length=120),
    nice_class: int | None = Query(None, ge=1, le=45),
    status: str | None = Query(None),
    has_logo: bool | None = Query(None),
    sort: str = Query("id"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
    session: AsyncSession = Depends(get_session),
):
    filters = []
    if q:
        like = f"%{q}%"
        filters.append(Mark.mark_text.ilike(like) | Mark.goods_description.ilike(like) | Mark.owner_name.ilike(like))
    if nice_class:
        filters.append(Mark.nice_class == nice_class)
    if status:
        filters.append(Mark.status == status)
    if has_logo is not None:
        filters.append(Mark.logo_svg.isnot(None) if has_logo else Mark.logo_svg.is_(None))

    total = (await session.execute(select(func.count(Mark.id)).where(*filters))).scalar_one()
    col = SORTS.get(sort, Mark.id)
    stmt = (select(Mark).where(*filters).order_by(col.desc() if order == "desc" else col.asc(), Mark.id)
            .offset((page - 1) * page_size).limit(page_size))
    rows = (await session.execute(stmt)).scalars().all()
    return {"items": [_out(m) for m in rows], "total": total, "page": page, "page_size": page_size}


@router.get("/marks/{mark_id}", response_model=MarkOut)
async def get_mark(mark_id: int, session: AsyncSession = Depends(get_session)):
    m = await session.get(Mark, mark_id)
    if m is None:
        raise HTTPException(404, "Mark not found")
    return _out(m)
