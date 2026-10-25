"""Main seeder: generates all synthetic data, embeds it, and bulk-inserts into PostgreSQL."""
import asyncio
import logging
import random
import time

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine

from app import dependencies as deps
from app.database import vec
from app.matchers.phonetic import phonetic_keys
from app.seed.decisions import chunk_text, generate_decisions
from app.seed.logos import assign_logos
from app.seed.marks import generate_marks
from app.seed.nice_classes import nice_reference_entries

log = logging.getLogger(__name__)

SEED = 42
N_MARKS = 5000
N_LOGOS = 2000
N_DECISIONS = 200


def build_dataset() -> dict:
    """Generate everything and compute embeddings (CPU/GPU-bound, run in a thread)."""
    rng = random.Random(SEED)
    t0 = time.time()
    marks = generate_marks(rng, N_MARKS)
    assign_logos(rng, marks, N_LOGOS)
    decisions = generate_decisions(rng, marks, N_DECISIONS)
    nice = nice_reference_entries()
    log.info("Generated synthetic records in %.1fs", time.time() - t0)

    deps.load_models()

    t0 = time.time()
    name_emb = deps.embed_texts([m["mark_text"] for m in marks])
    goods_emb = deps.embed_texts([m["goods_description"] for m in marks])
    for m, ne, ge in zip(marks, name_emb, goods_emb):
        m["text_embedding"] = vec(ne)
        m["goods_embedding"] = vec(ge)
        m["phonetic_keys"] = phonetic_keys(m["mark_text"])
    log.info("Embedded mark names + goods in %.1fs", time.time() - t0)

    t0 = time.time()
    logo_idx = [i for i, m in enumerate(marks) if m["logo_svg"]]
    images = [deps.svg_to_image(marks[i]["logo_svg"]) for i in logo_idx]
    logo_emb = deps.embed_images(images)
    for i in range(len(marks)):
        marks[i]["logo_embedding"] = None
    for i, e in zip(logo_idx, logo_emb):
        marks[i]["logo_embedding"] = vec(e)
    log.info("Rendered + CLIP-embedded %d logos in %.1fs", len(logo_idx), time.time() - t0)

    nice_emb = deps.embed_texts([n["description"] for n in nice])
    for n, e in zip(nice, nice_emb):
        n["embedding"] = vec(e)

    chunks = []
    for d in decisions:
        for ci, passage in enumerate(chunk_text(d["reasoning_text"])):
            chunks.append({**{k: d[k] for k in ("proceeding_number", "decision_date", "mark_a", "mark_b", "outcome")},
                           "chunk_index": ci, "text": passage})
    chunk_emb = deps.embed_texts([c["text"] for c in chunks])
    for c, e in zip(chunks, chunk_emb):
        c["embedding"] = vec(e)

    return {"marks": marks, "logos": len(logo_idx), "decisions": decisions, "chunks": chunks, "nice": nice}


INSERT_MARK = text(
    """
    INSERT INTO marks (mark_text, nice_class, goods_description, status, owner_name, filing_date, logo_svg,
                       phonetic_keys, text_embedding, goods_embedding, logo_embedding)
    VALUES (:mark_text, :nice_class, :goods_description, :status, :owner_name, :filing_date, :logo_svg,
            CAST(:phonetic_keys AS jsonb), CAST(:text_embedding AS vector), CAST(:goods_embedding AS vector),
            CAST(:logo_embedding AS vector))
    """
)
INSERT_CHUNK = text(
    """
    INSERT INTO precedent_chunks (proceeding_number, decision_date, mark_a, mark_b, outcome, chunk_index, text, embedding)
    VALUES (:proceeding_number, :decision_date, :mark_a, :mark_b, :outcome, :chunk_index, :text, CAST(:embedding AS vector))
    """
)
INSERT_NICE = text(
    """
    INSERT INTO nice_classes (class_number, class_name, description, embedding)
    VALUES (:class_number, :class_name, :description, CAST(:embedding AS vector))
    """
)


async def run_seed(engine: AsyncEngine) -> None:
    import json

    data = await asyncio.to_thread(build_dataset)
    mark_rows = [
        {k: m[k] for k in ("mark_text", "nice_class", "goods_description", "status", "owner_name", "filing_date",
                           "logo_svg", "text_embedding", "goods_embedding", "logo_embedding")}
        | {"phonetic_keys": json.dumps(m["phonetic_keys"])}
        for m in data["marks"]
    ]
    t0 = time.time()
    async with engine.begin() as conn:
        for i in range(0, len(mark_rows), 500):
            await conn.execute(INSERT_MARK, mark_rows[i : i + 500])
        await conn.execute(INSERT_CHUNK, data["chunks"])
        await conn.execute(INSERT_NICE, data["nice"])
        await conn.execute(text("ANALYZE marks"))
    log.info("Inserted into PostgreSQL in %.1fs", time.time() - t0)
    print(
        f"Seeded {len(data['marks'])} marks, {data['logos']} logos, {len(data['decisions'])} decisions, "
        f"{len(data['nice'])} class refs",
        flush=True,
    )


async def is_empty(engine: AsyncEngine) -> bool:
    async with engine.connect() as conn:
        count = (await conn.execute(text("SELECT count(*) FROM marks"))).scalar_one()
    return count == 0


if __name__ == "__main__":
    # Manual run: python -m app.seed.seed  (seeds only if the marks table is empty)
    from app.database import engine

    async def _main():
        if await is_empty(engine):
            await run_seed(engine)
        else:
            print("marks table is not empty; skipping seed")
        await engine.dispose()

    logging.basicConfig(level=logging.INFO)
    asyncio.run(_main())
