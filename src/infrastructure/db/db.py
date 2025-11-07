from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from infrastructure.settings.settings import settings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

async_engine = create_async_engine(
    url=settings.db.DATABASE_URL_asyncpg,
    pool_size=5,
    max_overflow=10
    )

session_fabric = async_sessionmaker(async_engine,expire_on_commit=False)

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_fabric() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            pass