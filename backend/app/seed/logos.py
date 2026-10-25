"""Procedural SVG logo generator: 1-3 geometric shapes plus optional mark text, 200x200 viewBox."""
import math
import random

SHAPES = ["circle", "triangle", "rectangle", "star", "hexagon"]
PALETTE = [
    "#e63946", "#f1a208", "#2a9d8f", "#264653", "#e76f51", "#457b9d", "#8338ec", "#3a86ff",
    "#ff006e", "#06d6a0", "#118ab2", "#073b4c", "#ef476f", "#ffd166", "#6a994e", "#bc4749",
    "#1d3557", "#f4a261", "#9b5de5", "#00bbf9",
]
FONT_WEIGHTS = [300, 400, 600, 700, 900]


def _polygon(cx: float, cy: float, r: float, n: int, rot: float = -90.0) -> str:
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def _star(cx: float, cy: float, r: float, points: int = 5) -> str:
    pts = []
    for i in range(points * 2):
        rr = r if i % 2 == 0 else r * 0.45
        a = math.radians(-90 + 180.0 * i / points)
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return " ".join(pts)


def _shape_svg(s: dict) -> str:
    kind, cx, cy, r, fill, op = s["kind"], s["cx"], s["cy"], s["r"], s["fill"], s["opacity"]
    if kind == "circle":
        return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}"/>'
    if kind == "rectangle":
        w, h = r * 1.8, r * 1.3
        return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" '
                f'rx="{s["rx"]}" fill="{fill}" fill-opacity="{op}"/>')
    if kind == "triangle":
        return f'<polygon points="{_polygon(cx, cy, r, 3)}" fill="{fill}" fill-opacity="{op}"/>'
    if kind == "hexagon":
        return f'<polygon points="{_polygon(cx, cy, r, 6, 0)}" fill="{fill}" fill-opacity="{op}"/>'
    return f'<polygon points="{_star(cx, cy, r)}" fill="{fill}" fill-opacity="{op}"/>'


def logo_spec(rng: random.Random, with_text: bool | None = None) -> dict:
    shapes = []
    for _ in range(rng.randint(1, 3)):
        shapes.append(
            {
                "kind": rng.choice(SHAPES),
                "cx": rng.uniform(60, 140),
                "cy": rng.uniform(55, 120),
                "r": rng.uniform(30, 70),
                "fill": rng.choice(PALETTE),
                "opacity": rng.choice([1, 0.9, 0.75]),
                "rx": rng.choice([0, 0, 8, 16]),
            }
        )
    return {
        "bg": rng.choice(["#ffffff", "#ffffff", "#f8f9fa", "#111827", "#fef3c7"]),
        "shapes": shapes,
        "text": rng.random() < 0.6 if with_text is None else with_text,
        "font_weight": rng.choice(FONT_WEIGHTS),
        "text_fill": rng.choice(["#111827", "#1f2937", "#ffffff", "#264653"]),
    }


def perturb_spec(rng: random.Random, spec: dict) -> dict:
    """A near-copy of a logo spec: same composition, nudged positions and maybe one colour change."""
    new = {**spec, "shapes": [dict(s) for s in spec["shapes"]]}
    for s in new["shapes"]:
        s["cx"] += rng.uniform(-8, 8)
        s["cy"] += rng.uniform(-8, 8)
        s["r"] *= rng.uniform(0.9, 1.1)
    if rng.random() < 0.5:
        rng.choice(new["shapes"])["fill"] = rng.choice(PALETTE)
    return new


def render_svg(spec: dict, mark_text: str) -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">',
        f'<rect width="200" height="200" fill="{spec["bg"]}"/>',
    ]
    parts += [_shape_svg(s) for s in spec["shapes"]]
    if spec["text"]:
        text_fill = spec["text_fill"]
        if spec["bg"] == "#111827" and text_fill != "#ffffff":
            text_fill = "#ffffff"
        size = max(16, min(30, int(260 / max(len(mark_text), 1))))
        parts.append(
            f'<text x="100" y="182" text-anchor="middle" font-family="DejaVu Sans, Arial, sans-serif" '
            f'font-size="{size}" font-weight="{spec["font_weight"]}" fill="{text_fill}">{mark_text.upper()}</text>'
        )
    parts.append("</svg>")
    return "".join(parts)


def assign_logos(rng: random.Random, records: list[dict], count: int = 2000) -> None:
    """Attach logo_svg to `count` of the records in place. Members of a collision group
    often get a perturbed copy of the group's first logo, so visual conflicts exist too."""
    chosen = set(rng.sample(range(len(records)), min(count, len(records))))
    group_specs: dict[int, dict] = {}
    for i, rec in enumerate(records):
        if i not in chosen:
            rec["logo_svg"] = None
            continue
        g = rec.get("collision_group")
        if g is not None and g in group_specs and rng.random() < 0.6:
            spec = perturb_spec(rng, group_specs[g])
        else:
            spec = logo_spec(rng)
            if g is not None:
                group_specs.setdefault(g, spec)
        rec["logo_svg"] = render_svg(spec, rec["mark_text"])
