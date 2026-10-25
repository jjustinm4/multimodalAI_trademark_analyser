"""Fake TTAB opposition decisions for RAG, built from templates with variable substitution."""
import random
from datetime import date

from app.seed.marks import random_date
from app.seed.nice_classes import NICE_HEADINGS

INTRO = [
    "{opposer} (\"Opposer\") has opposed registration of the mark {mark_b} for {goods_b} in International Class {class_b}, "
    "filed by {applicant} (\"Applicant\"). Opposer pleads priority and likelihood of confusion under Section 2(d) of the "
    "Trademark Act, based on its prior registration of the mark {mark_a} for {goods_a} in International Class {class_a}. "
    "The case is fully briefed. Having considered the record and the arguments of the parties, we {verdict_word} the opposition.",
    "This proceeding concerns Applicant {applicant}'s application to register {mark_b} for {goods_b}. Opposer {opposer} "
    "relies on its registered mark {mark_a}, used in connection with {goods_a}. The sole issue before the Board is whether "
    "the applied-for mark, when used on the identified goods and services, is likely to cause confusion with Opposer's mark. "
    "For the reasons set out below, the opposition is {outcome}.",
    "{opposer} filed a notice of opposition against Application Serial No. {serial} for the mark {mark_b}. Opposer asserts "
    "that Applicant's mark so resembles Opposer's previously registered mark {mark_a} as to be likely, when used on or in "
    "connection with Applicant's goods, to cause confusion, mistake, or deception. Applicant denied the salient allegations. "
    "Our analysis is guided by the factors set forth in In re E. I. du Pont de Nemours & Co.",
]

SIMILARITY = {
    "high": [
        "Turning first to the similarity of the marks, we compare them in their entireties as to appearance, sound, connotation "
        "and commercial impression. {mark_a} and {mark_b} differ by only {diff}. When spoken, the marks are nearly "
        "indistinguishable; consumers who encounter the marks at different times are unlikely to recall the minor difference. "
        "Neither mark has a recognised meaning in English, so neither connotation distinguishes them. Where marks are coined "
        "terms of this kind, the overall sound and visual cadence carry particular weight. This factor weighs heavily in favour "
        "of finding a likelihood of confusion.",
        "The marks {mark_a} and {mark_b} share the same structure and dominant syllables. Applicant argues that the {diff} "
        "creates a distinct impression, but we are not persuaded. The test is not whether the marks can be distinguished in a "
        "side-by-side comparison, but whether they are sufficiently similar in overall commercial impression that persons who "
        "encounter them would be likely to assume a connection. Phonetic identity, or near identity, is often sufficient on its "
        "own. We find the marks highly similar.",
    ],
    "low": [
        "Turning to the marks, Opposer emphasises that {mark_a} and {mark_b} share certain letters. However, marks must be "
        "considered in their entireties. Here the {diff} produces a different cadence and a different overall impression. "
        "The shared elements are common building blocks found in many registered marks, which diminishes their source-identifying "
        "capacity. We find that the differences outweigh the similarities, and this factor weighs against a finding of confusion.",
        "Although both marks are coined terms, {mark_a} and {mark_b} differ in sound and appearance because of the {diff}. "
        "Consumers are generally attentive to the beginnings of marks, and the overall rhythm of the two marks is distinct. "
        "On this record, the marks are more dissimilar than similar.",
    ],
}

GOODS = {
    "related": [
        "As to the relatedness of the goods and services, we must consider them as they are identified in the application and "
        "registration. Opposer's {goods_a} and Applicant's {goods_b} are complementary and are of a type commonly offered under a "
        "single mark. The record contains third-party registrations covering both types of goods, which suggests that consumers "
        "would expect them to emanate from the same source. Because neither identification is limited as to channels of trade, "
        "we presume the goods travel in all normal channels to all usual purchasers. These factors favour Opposer.",
        "The goods need not be identical to support a finding of likelihood of confusion; it is enough that they are related in "
        "some manner, or that the circumstances surrounding their marketing are such that they would be encountered by the same "
        "persons under conditions giving rise to a mistaken belief of a common source. Here, {goods_a} and {goods_b} are offered "
        "to overlapping classes of consumers through the same online channels. The relatedness factor weighs in favour of Opposer.",
    ],
    "unrelated": [
        "Opposer has not shown that {goods_a} and {goods_b} are related. The goods fall in different classes, serve different "
        "purposes, and the record contains no evidence that a single source commonly offers both under the same mark. "
        "Classification alone is not determinative, but Opposer bears the burden of establishing relatedness and has not done so. "
        "This factor weighs against a likelihood of confusion.",
        "We find that the goods and services at issue are distinct. Applicant's {goods_b} are directed to a different market than "
        "Opposer's {goods_a}, and the evidence of overlapping trade channels is thin. Mere speculation that a consumer might "
        "encounter both is insufficient. This factor favours Applicant.",
    ],
}

STRENGTH = {
    "strong": [
        "Regarding the strength of Opposer's mark, {mark_a} is a coined term with no descriptive meaning, and is therefore "
        "inherently distinctive. Opposer has also submitted evidence of use since {year_a}, including advertising expenditure and "
        "unsolicited media coverage. Applicant introduced no evidence of third-party use of similar marks. We accord {mark_a} a "
        "normal-to-broad scope of protection.",
        "Opposer's mark is arbitrary as applied to its goods and is conceptually strong. There is no evidence of a crowded field "
        "of similar marks for related goods. Accordingly, Opposer's mark is entitled to the full scope of protection afforded "
        "inherently distinctive marks.",
    ],
    "weak": [
        "Applicant submitted evidence of numerous third-party registrations and uses of marks containing elements similar to "
        "{mark_a} for related goods. Such evidence shows that consumers have become accustomed to distinguishing between marks "
        "based on small differences. The commercial strength of Opposer's mark is therefore limited, and its scope of protection "
        "is correspondingly narrow.",
        "While {mark_a} is inherently distinctive, the record shows a crowded field of similar coined marks in this sector. This "
        "weakens Opposer's mark and suggests that consumers look to other elements to distinguish source.",
    ],
}

PURCHASE = {
    "casual": [
        "As to the conditions of purchase, the goods at issue are relatively inexpensive and may be purchased on impulse without "
        "careful deliberation. Where goods are subject to such casual purchase, the risk of confusion increases. This factor "
        "favours a finding of likelihood of confusion.",
    ],
    "careful": [
        "As to the conditions of purchase, the goods and services are typically purchased by sophisticated, professional buyers "
        "after careful evaluation, often under negotiated contracts. Such purchasers are less likely to be confused by similar "
        "marks. This factor weighs slightly against a finding of likelihood of confusion.",
    ],
}

CONCLUSION = {
    "sustained": [
        "Having considered all of the evidence and arguments bearing on the du Pont factors, we conclude that Applicant's mark "
        "{mark_b}, used in connection with the identified goods, so resembles Opposer's registered mark {mark_a} as to be likely "
        "to cause confusion. To the extent any doubt exists, it is resolved in favour of the prior registrant. "
        "Decision: The opposition is sustained and registration to Applicant is refused.",
    ],
    "dismissed": [
        "Weighing all of the relevant du Pont factors, we find that Opposer has not established by a preponderance of the evidence "
        "that Applicant's mark {mark_b} is likely to cause confusion with Opposer's mark {mark_a}. The differences between the "
        "marks and the goods are sufficient to avoid confusion. Decision: The opposition is dismissed.",
    ],
}


def _describe_diff(a: str, b: str) -> str:
    a, b = a.lower(), b.lower()
    if len(a) != len(b):
        return "addition or omission of a single letter" if abs(len(a) - len(b)) == 1 else "difference in length and ending"
    diffs = sum(1 for x, y in zip(a, b) if x != y)
    if diffs == 1:
        return "substitution of a single letter"
    return f"difference in {diffs} letters"


def generate_decisions(rng: random.Random, marks: list[dict], n: int = 200) -> list[dict]:
    """Build n decisions. Most pair marks from the same collision group; a few pair unrelated marks."""
    groups: dict[int, list[dict]] = {}
    for m in marks:
        if m.get("collision_group") is not None:
            groups.setdefault(m["collision_group"], []).append(m)
    group_list = [g for g in groups.values() if len(g) >= 2]

    used_numbers: set[str] = set()
    decisions = []
    for _ in range(n):
        if group_list and rng.random() < 0.85:
            a, b = rng.sample(rng.choice(group_list), 2)
        else:
            a, b = rng.sample(marks, 2)

        same_family = a.get("collision_group") is not None and a.get("collision_group") == b.get("collision_group")
        related = a["nice_class"] == b["nice_class"] or rng.random() < 0.3
        strong = rng.random() < 0.6
        careful = rng.random() < 0.35
        # Outcome follows the factors, with a little noise.
        score = (2 if same_family else -1) + (1.5 if related else -1.5) + (0.5 if strong else -0.5) + (-0.5 if careful else 0.5)
        outcome = "sustained" if score + rng.uniform(-0.8, 0.8) > 1.0 else "dismissed"

        while True:
            num = f"91{rng.randint(0, 999999):06d}"
            if num not in used_numbers:
                used_numbers.add(num)
                break
        filing_a = a["filing_date"]
        dec_date = random_date(rng, start=max(filing_a, date(2016, 6, 1)), end=date(2026, 9, 30))

        ctx = {
            "mark_a": a["mark_text"].upper(), "mark_b": b["mark_text"].upper(),
            "goods_a": a["goods_description"], "goods_b": b["goods_description"],
            "class_a": a["nice_class"], "class_b": b["nice_class"],
            "class_a_name": NICE_HEADINGS[a["nice_class"]][0],
            "opposer": a["owner_name"], "applicant": b["owner_name"],
            "serial": f"{rng.randint(86, 99)}{rng.randint(0, 999999):06d}",
            "diff": _describe_diff(a["mark_text"], b["mark_text"]),
            "year_a": filing_a.year, "outcome": outcome,
            "verdict_word": "sustain" if outcome == "sustained" else "dismiss",
        }
        paras = [rng.choice(INTRO), rng.choice(SIMILARITY["high" if same_family else "low"]),
                 rng.choice(GOODS["related" if related else "unrelated"])]
        if rng.random() < 0.8:
            paras.append(rng.choice(STRENGTH["strong" if strong else "weak"]))
        if rng.random() < 0.6:
            paras.append(rng.choice(PURCHASE["careful" if careful else "casual"]))
        paras.append(rng.choice(CONCLUSION[outcome]))
        # Keep 3-5 paragraphs, always ending with the conclusion.
        if len(paras) > 5:
            paras = paras[:4] + paras[-1:]

        decisions.append(
            {
                "proceeding_number": num,
                "decision_date": dec_date,
                "mark_a": ctx["mark_a"],
                "mark_b": ctx["mark_b"],
                "outcome": outcome,
                "reasoning_text": "\n\n".join(p.format(**ctx) for p in paras),
            }
        )
    return decisions


def chunk_text(text: str, max_tokens: int = 500) -> list[str]:
    """Split on paragraph boundaries into ~max_tokens passages (tokens ~= words * 1.33)."""
    max_words = int(max_tokens / 1.33)
    chunks, current, count = [], [], 0
    for para in text.split("\n\n"):
        words = len(para.split())
        if current and count + words > max_words:
            chunks.append("\n\n".join(current))
            current, count = [], 0
        current.append(para)
        count += words
    if current:
        chunks.append("\n\n".join(current))
    return chunks
