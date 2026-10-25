"""Absolute grounds screener. Rule-based: descriptiveness, prohibited terms, single letter / numerals."""
import logging
import re
from functools import lru_cache

from rapidfuzz import fuzz, process

from app.screener.prohibited import TERM_CATEGORY, TERMS

log = logging.getLogger(__name__)

PROHIBITED_THRESHOLD = 85


@lru_cache(maxsize=1)
def _wordnet():
    try:
        from nltk.corpus import wordnet

        wordnet.ensure_loaded()
        return wordnet
    except LookupError:
        try:
            import nltk

            nltk.download("wordnet", quiet=True)
            from nltk.corpus import wordnet

            wordnet.ensure_loaded()
            return wordnet
        except Exception:  # noqa: BLE001
            log.warning("WordNet unavailable; descriptiveness check disabled")
            return None


def tokenize(mark_text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", mark_text.lower())


def is_dictionary_word(token: str) -> bool:
    wn = _wordnet()
    if wn is None or len(token) < 2 or token.isdigit():
        return False
    return bool(wn.synsets(token))


def _prohibited_match(mark_text: str, tokens: list[str]) -> tuple[str, float] | None:
    """Fuzzy-match the mark (and each run of its words) against the prohibited list.
    Short acronyms (<=4 letters, e.g. FBI, NASA) must match a whole word exactly so
    coined marks like 'Ciatek' are not flagged for 'CIA'."""
    if not tokens:
        return None
    windows = {" ".join(tokens[i:j]) for i in range(len(tokens)) for j in range(i + 1, len(tokens) + 1)}
    windows.add("".join(tokens))
    best: tuple[str, float] | None = None
    for w in windows:
        for term, score, _ in process.extract(w, TERMS, scorer=fuzz.ratio, processor=str.lower, limit=3,
                                              score_cutoff=PROHIBITED_THRESHOLD):
            if len(term.replace(" ", "")) <= 4 and w != term.lower():
                continue
            if best is None or score > best[1]:
                best = (term, score)
    return best


def screen(mark_text: str) -> dict:
    tokens = tokenize(mark_text)
    flags: list[str] = []

    dict_tokens = [t for t in tokens if is_dictionary_word(t)]
    descriptive = len(tokens) >= 2 and len(dict_tokens) / len(tokens) >= 0.5
    if descriptive:
        flags.append(f"Potentially descriptive: {len(dict_tokens)} of {len(tokens)} words are dictionary words "
                     f"({', '.join(dict_tokens)})")

    prohibited = _prohibited_match(mark_text, tokens)
    if prohibited:
        term, score = prohibited
        flags.append(f"Prohibited term: resembles \"{term}\" ({TERM_CATEGORY[term]}, {score:.0f}% match)")

    compact = "".join(tokens)
    if len(compact) == 1:
        flags.append("Single character mark: lacks inherent distinctiveness")
    elif compact.isdigit():
        flags.append("Purely numeric mark: lacks inherent distinctiveness")

    return {
        "descriptive": descriptive,
        "prohibited_match": prohibited[0] if prohibited else None,
        "prohibited_score": round(prohibited[1], 1) if prohibited else None,
        "flags": flags,
        "dictionary_tokens": dict_tokens,
        "tokens": tokens,
    }
