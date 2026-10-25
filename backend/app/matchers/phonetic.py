"""Phonetic matcher: Double Metaphone + Soundex keys, scored with rapidfuzz and Jaro-Winkler.

Deterministic, no model. Double Metaphone comes from the `metaphone` package
(jellyfish ships Soundex/Metaphone/NYSIIS but not Double Metaphone).
"""
import re

import jellyfish
from metaphone import doublemetaphone
from rapidfuzz import fuzz
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


def normalise(mark: str) -> str:
    return re.sub(r"[^a-z0-9]", "", mark.lower())


def phonetic_keys(mark: str) -> list[str]:
    """Keys stored in marks.phonetic_keys, e.g. ["DM:SNTR", "SX:Z536"]."""
    word = normalise(mark)
    if not word:
        return []
    keys = []
    primary, secondary = doublemetaphone(word)
    for k in (primary, secondary):
        if k:
            keys.append(f"DM:{k}")
    keys.append(f"SX:{jellyfish.soundex(word)}")
    return sorted(set(keys))


def phonetic_score(query: str, candidate: str) -> float:
    q, c = normalise(query), normalise(candidate)
    if not q or not c:
        return 0.0
    ratio = fuzz.ratio(q, c) / 100.0
    jw = jellyfish.jaro_winkler_similarity(q, c)
    return max(ratio, jw)


async def match(session: AsyncSession, mark_text: str, limit: int = 100) -> list[dict]:
    keys = phonetic_keys(mark_text)
    if not keys:
        return []
    rows = (
        await session.execute(
            text("SELECT id, mark_text FROM marks WHERE phonetic_keys ?| CAST(:keys AS text[])"),
            {"keys": keys},
        )
    ).all()
    scored = [{"id": r.id, "mark_text": r.mark_text, "score": phonetic_score(mark_text, r.mark_text)} for r in rows]
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:limit]
