"""Fusion scorer: configurable weighted average of the four matcher scores."""
from app.config import settings

MATCHERS = ("phonetic", "semantic", "visual", "goods")


def weights(use_visual: bool, include: tuple[str, ...] = MATCHERS) -> dict[str, float]:
    """Weights from env. Matchers not in use have their weight redistributed proportionally."""
    base = {
        "phonetic": settings.fusion_w_phonetic,
        "semantic": settings.fusion_w_semantic,
        "visual": settings.fusion_w_visual,
        "goods": settings.fusion_w_goods,
    }
    active = {k: v for k, v in base.items() if k in include and (use_visual or k != "visual")}
    total = sum(active.values()) or 1.0
    return {k: v / total for k, v in active.items()}


def fuse(
    results: dict[str, list[dict]],
    goods_scores: dict[int, float] | None,
    use_visual: bool,
    top_k: int = 25,
    include: tuple[str, ...] = MATCHERS,
) -> tuple[list[dict], dict[str, float]]:
    """results: {matcher: [{id, mark_text, score}]}. Returns (ranked candidates, weights used)."""
    w = weights(use_visual, include)
    table: dict[int, dict] = {}
    for name, hits in results.items():
        for h in hits:
            row = table.setdefault(h["id"], {"id": h["id"], "mark_text": h["mark_text"],
                                             "scores": {k: 0.0 for k in w}})
            if name in row["scores"]:
                row["scores"][name] = max(row["scores"][name], h["score"])
    if goods_scores is not None and "goods" in w:
        for cid, row in table.items():
            row["scores"]["goods"] = goods_scores.get(cid, 0.0)

    for row in table.values():
        row["contributions"] = {k: w[k] * row["scores"].get(k, 0.0) for k in w}
        row["final_score"] = sum(row["contributions"].values())

    ranked = sorted(table.values(), key=lambda r: r["final_score"], reverse=True)
    return ranked[:top_k], w
