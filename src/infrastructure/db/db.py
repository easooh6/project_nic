from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from src.infrastructure.settings.settings import settings
from collections.abc import AsyncGenerator

async_engine = create_async_engine(
    url=settings.db.DATABASE_URL_asyncpg,
    pool_size=5,
    max_overflow=10
)

session_factory = async_sessionmaker(async_engine, expire_on_commit=False)


def get_db_session():
    """Return session factory for dependency injection"""
    return session_factory