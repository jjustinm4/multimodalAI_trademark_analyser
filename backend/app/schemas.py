from datetime import date

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    mark_text: str = Field(min_length=1, max_length=120)
    goods_description: str = Field(min_length=1, max_length=2000)
    nice_class: int | None = Field(default=None, ge=1, le=45)
    # base64 image, optionally as a data URL ("data:image/png;base64,...")
    logo_file: str | None = None


class ClassifyRequest(BaseModel):
    goods_description: str = Field(min_length=1, max_length=2000)


class MatcherScores(BaseModel):
    phonetic: float = 0.0
    semantic: float = 0.0
    visual: float = 0.0
    goods: float = 0.0


class Citation(BaseModel):
    id: int
    mark_text: str
    nice_class: int
    goods_description: str
    status: str
    owner_name: str
    logo_svg: str | None = None
    scores: MatcherScores
    contributions: MatcherScores  # weight * score, sums to final_score
    final_score: float


class ClassSuggestion(BaseModel):
    class_number: int
    class_name: str
    confidence: float


class NiceClassResult(BaseModel):
    top_classes: list[ClassSuggestion]
    provided_class: int | None = None
    matches_top: bool | None = None


class GroundsResult(BaseModel):
    descriptive: bool
    prohibited_match: str | None = None
    flags: list[str]
    dictionary_tokens: list[str] = []
    tokens: list[str] = []
    prohibited_score: float | None = None


class Precedent(BaseModel):
    proceeding_number: str
    decision_date: date
    mark_a: str
    mark_b: str
    outcome: str
    excerpt: str
    similarity: float


class AnalyzeResponse(BaseModel):
    query: dict
    weights: dict[str, float]
    citations: list[Citation]
    nice_class: NiceClassResult
    grounds: GroundsResult
    precedent: list[Precedent]
    report: str
    report_source: str  # "llm" or "fallback"
    report_warning: str | None = None
    timings_ms: dict[str, float]


class SearchResult(BaseModel):
    id: int
    mark_text: str
    nice_class: int
    goods: str
    status: str
    similarity: float
    phonetic: float
    semantic: float


class SearchResponse(BaseModel):
    results: list[SearchResult]


class ClassifyResponse(BaseModel):
    top_classes: list[ClassSuggestion]


class MarkOut(BaseModel):
    id: int
    mark_text: str
    nice_class: int
    goods_description: str
    status: str
    owner_name: str
    filing_date: date
    logo_svg: str | None = None
    phonetic_keys: list[str] = []


class MarkPage(BaseModel):
    items: list[MarkOut]
    total: int
    page: int
    page_size: int
