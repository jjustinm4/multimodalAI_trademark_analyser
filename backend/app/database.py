from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

engine = create_async_engine(settings.database_url, pool_size=10, max_overflow=10)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with SessionLocal() as session:
        yield session


def vec(values) -> str:
    """Format a vector as a pgvector text literal. Used with CAST(:v AS vector)."""
    return "[" + ",".join(f"{float(x):.6f}" for x in values) + "]"
