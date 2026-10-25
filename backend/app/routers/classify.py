"""POST /api/classify — Nice classification only."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.classifier import nice
from app.database import get_session
from app.schemas import ClassifyRequest, ClassifyResponse

router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse)
async def classify(req: ClassifyRequest, session: AsyncSession = Depends(get_session)):
    return {"top_classes": await nice.classify(session, req.goods_description)}
