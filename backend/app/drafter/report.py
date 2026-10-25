"""Report drafter: calls llama-server (OpenAI-compatible) to write the examination report.
Falls back to a template report if the LLM is unreachable or returns nothing."""
import logging
from datetime import date

import httpx

from app.config import settings

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """Reasoning: low

You are a trademark examining attorney drafting a first-action examination report.
Use ONLY the evidence provided in the user message. Do not invent marks, registrations,
proceedings, owners, dates or facts. Cite prior marks by name and registration ID exactly as given,
and cite precedent by proceeding number exactly as given. If the evidence is weak, say so.

Write the report in Markdown with exactly these sections:

## Summary
One short paragraph: the applied-for mark, its class, and the overall recommendation
(REFUSE under Section 2(d), ISSUE REQUIREMENT, or APPROVE FOR PUBLICATION).

## Section 2(d) Likelihood of Confusion
Discuss the most relevant cited marks (at most 5). For each: similarity of the marks
(sound, appearance, meaning) using the phonetic/semantic/visual scores, and relatedness of
the goods using the goods score. Then state a conclusion.

## Absolute Grounds
Address descriptiveness, prohibited or protected terms, and single-character/numeric issues,
using only the screening results provided.

## Classification
Comment on whether the stated class fits the goods, using the suggested classes.

## Supporting Precedent
Briefly relate each provided precedent passage to this application.

## Recommendation
A numbered list of concrete next steps for the examiner or applicant.

Keep the report under 700 words. Use a formal, neutral register."""


def _fmt_citation(i: int, c: dict) -> str:
    s = c["scores"]
    return (
        f"{i}. {c['mark_text'].upper()} (Reg. ID {c['id']}), Class {c['nice_class']}, status: {c['status']}, "
        f"owner: {c['owner_name']}\n"
        f"   Goods: {c['goods_description']}\n"
        f"   Scores: overall {c['final_score']:.2f}; phonetic {s['phonetic']:.2f}, semantic {s['semantic']:.2f}, "
        f"visual {s['visual']:.2f}, goods {s['goods']:.2f}"
    )


def build_user_message(query: dict, citations: list[dict], grounds: dict, nice: dict, precedent: list[dict]) -> str:
    lines = [
        "APPLIED-FOR MARK",
        f"Mark: {query['mark_text'].upper()}",
        f"Goods/services: {query['goods_description']}",
        f"Stated class: {query.get('nice_class') or 'not stated'}",
        f"Logo submitted: {'yes' if query.get('has_logo') else 'no'}",
        "",
        "CITED PRIOR MARKS (ranked by fused similarity, 0-1)",
    ]
    lines += [_fmt_citation(i, c) for i, c in enumerate(citations, 1)] or ["None found."]
    lines += ["", "ABSOLUTE GROUNDS SCREENING"]
    lines += [f"- {f}" for f in grounds["flags"]] or ["- No absolute grounds issues detected."]
    lines += ["", "SUGGESTED NICE CLASSES"]
    lines += [f"- Class {c['class_number']} ({c['class_name']}): confidence {c['confidence']:.2f}"
              for c in nice["top_classes"]]
    lines += ["", "PRECEDENT PASSAGES"]
    for p in precedent:
        lines.append(f"[{p['proceeding_number']}] {p['mark_a']} v. {p['mark_b']}, decided {p['decision_date']}, "
                     f"opposition {p['outcome']}:\n{p['excerpt']}")
    return "\n".join(lines)


def risk_level(citations: list[dict]) -> str:
    top = citations[0]["final_score"] if citations else 0.0
    return "HIGH" if top > 0.8 else "MEDIUM" if top >= 0.5 else "LOW"


def fallback_report(query: dict, citations: list[dict], grounds: dict, nice: dict, precedent: list[dict]) -> str:
    risk = risk_level(citations)
    rec = {"HIGH": "REFUSE under Section 2(d)", "MEDIUM": "ISSUE REQUIREMENT / further review",
           "LOW": "APPROVE FOR PUBLICATION"}[risk]
    if grounds["flags"] and risk == "LOW":
        rec = "ISSUE REQUIREMENT (absolute grounds)"
    mark = query["mark_text"].upper()
    out = [
        "## Summary",
        f"Application for **{mark}** covering \"{query['goods_description']}\" "
        f"(Class {query.get('nice_class') or 'not stated'}). Automated conflict risk: **{risk}**. "
        f"Provisional recommendation: **{rec}**.",
        "",
        "## Section 2(d) Likelihood of Confusion",
    ]
    if citations:
        for c in citations[:5]:
            s = c["scores"]
            out.append(f"- **{c['mark_text'].upper()}** (Reg. ID {c['id']}, Class {c['nice_class']}, {c['status']}): "
                       f"overall {c['final_score']:.2f} — phonetic {s['phonetic']:.2f}, semantic {s['semantic']:.2f}, "
                       f"visual {s['visual']:.2f}, goods {s['goods']:.2f}.")
    else:
        out.append("No similar prior marks were found.")
    out += ["", "## Absolute Grounds"]
    out += [f"- {f}" for f in grounds["flags"]] or ["- No absolute grounds issues detected."]
    out += ["", "## Classification"]
    out += [f"- Class {c['class_number']} ({c['class_name']}): confidence {c['confidence']:.2f}" for c in nice["top_classes"]]
    if nice.get("matches_top") is False:
        out.append(f"- The stated class ({query.get('nice_class')}) differs from the top suggestion; confirm classification.")
    out += ["", "## Supporting Precedent"]
    out += [f"- {p['proceeding_number']} ({p['mark_a']} v. {p['mark_b']}, {p['decision_date']}): opposition {p['outcome']}."
            for p in precedent] or ["- No precedent retrieved."]
    out += ["", "## Recommendation",
            "1. Review the top cited marks and confirm the similarity assessment.",
            "2. Confirm the identification of goods and the Nice class.",
            "3. Resolve any absolute grounds flags before approval.",
            "", f"_Template report generated {date.today().isoformat()} without the language model._"]
    return "\n".join(out)


async def draft(query: dict, citations: list[dict], grounds: dict, nice: dict, precedent: list[dict]) -> dict:
    """Returns {report, source: 'llm'|'fallback', warning}."""
    top = citations[:5]
    payload = {
        "model": settings.llm_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_message(query, top, grounds, nice, precedent)},
        ],
        "max_tokens": 2000,
        "temperature": 0.3,
    }
    try:
        async with httpx.AsyncClient(timeout=settings.llm_timeout_s) as client:
            r = await client.post(f"{settings.llm_base_url.rstrip('/')}/chat/completions", json=payload)
            r.raise_for_status()
            content = (r.json()["choices"][0]["message"].get("content") or "").strip()
        if not content:
            raise ValueError("LLM returned an empty report")
        return {"report": content, "source": "llm", "warning": None}
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as exc:
        log.warning("Report drafter falling back to template: %s", exc)
        return {
            "report": fallback_report(query, top, grounds, nice, precedent),
            "source": "fallback",
            "warning": f"Language model unavailable ({type(exc).__name__}). This is a template report, not an AI draft.",
        }
