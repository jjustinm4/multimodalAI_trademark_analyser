"""Smoke tests for each matcher and the generators. No database needed.

Run: cd backend && python -m pytest tests -q
Set RUN_MODEL_TESTS=1 to also load MiniLM/CLIP (downloads models on first run).
"""
import os
import random

import pytest

from app.drafter.report import fallback_report, risk_level
from app.matchers import fusion
from app.matchers.phonetic import phonetic_keys, phonetic_score
from app.screener.grounds import screen
from app.seed.decisions import chunk_text, generate_decisions
from app.seed.logos import assign_logos
from app.seed.marks import generate_marks, phonetic_variants
from app.seed.nice_classes import nice_reference_entries


# --- phonetic ---------------------------------------------------------------

def test_phonetic_keys_shared_for_sound_alikes():
    a, b = set(phonetic_keys("Zentara")), set(phonetic_keys("Sentara"))
    assert a & b, (a, b)


def test_phonetic_score_ranks_variants_above_unrelated():
    assert phonetic_score("Zentara", "Zentara") == 1.0
    assert phonetic_score("Zentara", "Sentara") > phonetic_score("Zentara", "Plexivo")
    assert 0.0 <= phonetic_score("abc", "xyz") <= 1.0


# --- fusion -----------------------------------------------------------------

def test_fusion_weights_redistribute_without_logo():
    w = fusion.weights(use_visual=False)
    assert "visual" not in w
    assert w["phonetic"] == pytest.approx(0.375)
    assert w["semantic"] == pytest.approx(0.375)
    assert w["goods"] == pytest.approx(0.25)
    assert sum(fusion.weights(use_visual=True).values()) == pytest.approx(1.0)


def test_fusion_unions_and_ranks():
    results = {
        "phonetic": [{"id": 1, "mark_text": "A", "score": 0.9}, {"id": 2, "mark_text": "B", "score": 0.4}],
        "semantic": [{"id": 2, "mark_text": "B", "score": 0.8}, {"id": 3, "mark_text": "C", "score": 0.7}],
        "visual": [],
    }
    ranked, w = fusion.fuse(results, {1: 0.9, 2: 0.1, 3: 0.2}, use_visual=False)
    ids = [r["id"] for r in ranked]
    assert set(ids) == {1, 2, 3}
    assert ids[0] == 1
    top = ranked[0]
    assert top["final_score"] == pytest.approx(sum(top["contributions"].values()))
    assert ranked[2]["scores"]["phonetic"] == 0.0  # missing scores filled with 0


# --- grounds ----------------------------------------------------------------

def test_grounds_prohibited_and_acronym_guard():
    assert screen("Champagne Nights")["prohibited_match"] == "Champagne"
    assert screen("Olympik")["prohibited_match"] == "Olympic"
    assert screen("Ciatek")["prohibited_match"] is None  # must not trip on "CIA"
    assert screen("Zentara")["flags"] == []


def test_grounds_single_char_and_numeric():
    assert any("Single character" in f for f in screen("X")["flags"])
    assert any("numeric" in f for f in screen("2024")["flags"])


def test_grounds_descriptive():
    try:
        from nltk.corpus import wordnet
        wordnet.ensure_loaded()
    except LookupError:
        pytest.skip("WordNet data not installed")
    r = screen("Fresh Coffee")
    assert r["descriptive"] is True
    assert screen("Zentara Plexivo")["descriptive"] is False


# --- generators -------------------------------------------------------------

def test_generators_deterministic_and_sized():
    a = generate_marks(random.Random(42), 5000)
    b = generate_marks(random.Random(42), 5000)
    assert len(a) == 5000
    assert [m["mark_text"] for m in a[:50]] == [m["mark_text"] for m in b[:50]]
    assert {m["nice_class"] for m in a} == set(range(1, 46))
    assert sum(1 for m in a if m["collision_group"] is not None) > 1000


def test_logos_and_decisions():
    rng = random.Random(7)
    marks = generate_marks(rng, 600)
    assign_logos(rng, marks, 200)
    assert sum(1 for m in marks if m["logo_svg"]) == 200
    svg = next(m["logo_svg"] for m in marks if m["logo_svg"])
    assert svg.startswith("<svg") and 'viewBox="0 0 200 200"' in svg
    decs = generate_decisions(rng, marks, 20)
    assert len(decs) == 20
    assert all(d["proceeding_number"].startswith("91") and len(d["proceeding_number"]) == 8 for d in decs)
    assert all(3 <= len(d["reasoning_text"].split("\n\n")) <= 5 for d in decs)
    assert all(len(c.split()) <= 400 for d in decs for c in chunk_text(d["reasoning_text"]))


def test_variants_and_nice_refs():
    v = phonetic_variants("Zentara", random.Random(1), 4)
    assert len(v) == 4 and "Zentara" not in v
    assert len(nice_reference_entries()) == 69


def test_fallback_report():
    cites = [{"id": 1, "mark_text": "Zentara", "nice_class": 9, "status": "registered", "owner_name": "X",
              "goods_description": "software", "final_score": 0.85,
              "scores": {"phonetic": 0.9, "semantic": 0.9, "visual": 0.0, "goods": 0.7}}]
    assert risk_level(cites) == "HIGH"
    text = fallback_report({"mark_text": "Sentara", "goods_description": "software", "nice_class": 9},
                           cites, screen("Sentara"), {"top_classes": []}, [])
    assert "## Summary" in text and "ZENTARA" in text


# --- models (optional) ------------------------------------------------------

@pytest.mark.skipif(not os.environ.get("RUN_MODEL_TESTS"), reason="set RUN_MODEL_TESTS=1")
def test_embedders():
    from app import dependencies as deps
    from app.seed.logos import logo_spec, render_svg

    e = deps.embed_texts(["Zentara", "Sentara"])
    assert e.shape == (2, 384)
    img = deps.svg_to_image(render_svg(logo_spec(random.Random(1)), "Zentara"))
    assert deps.embed_images([img]).shape == (1, 512)
