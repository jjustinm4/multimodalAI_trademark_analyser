"""FastAPI app. Lifespan runs the startup sequence: wait for DB, migrate, seed if empty, load models."""
import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app import dependencies as deps
from app.database import engine
from app.routers import analyze, classify, health, marks, search
from app.screener import grounds
from app.seed.seed import is_empty, run_seed

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("app")

BACKEND_DIR = Path(__file__).resolve().parent.parent


async def wait_for_db(retries: int = 30, delay: float = 2.0) -> None:
    for attempt in range(1, retries + 1):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return
        except Exception as exc:  # noqa: BLE001
            log.info("Waiting for PostgreSQL (%d/%d): %s", attempt, retries, exc)
            await asyncio.sleep(delay)
    raise RuntimeError("PostgreSQL did not become ready")


def run_migrations() -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.attributes["configure_logger"] = False
    command.upgrade(cfg, "head")


@asynccontextmanager
async def lifespan(_: FastAPI):
    await wait_for_db()
    # alembic's env.py calls asyncio.run, so it must run outside this event loop.
    await asyncio.to_thread(run_migrations)
    if await is_empty(engine):
        log.info("marks table is empty; seeding synthetic data (first boot)")
        await run_seed(engine)
    await asyncio.to_thread(deps.load_models)
    await asyncio.to_thread(grounds.screen, "warm up wordnet")  # first WordNet load takes ~2s
    async with engine.connect() as conn:
        count = (await conn.execute(text("SELECT count(*) FROM marks"))).scalar_one()
    print(f"Backend ready — models loaded, {count} marks indexed", flush=True)
    yield
    await engine.dispose()


app = FastAPI(title="Trademark Examination PoC", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

for r in (analyze, search, classify, marks, health):
    app.include_router(r.router, prefix="/api")
