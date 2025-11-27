from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy import text
from src.infrastructure.settings.settings import settings
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from src.logger.logger import setup_logging

logger = setup_logging("db")

_async_engine: AsyncEngine = None
_async_session_fabric = None

def get_session_fabric():

    if _async_session_fabric is None:
        raise RuntimeError("Database is not initialized.")
    
    return _async_session_fabric


async def init_db():

    global _async_engine, _async_session_fabric

    if _async_engine is None:
        _async_engine = create_async_engine(
        url=settings.db.DATABASE_URL_asyncpg,
        pool_size=5,
        max_overflow=10
        )
    
    async with _async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        logger.info("DB connection successfully established")

    if _async_session_fabric is None:
        _async_session_fabric = async_sessionmaker(_async_engine,expire_on_commit=False)
    
    
    return

async def close_db():

    if _async_engine:
        await _async_engine.dispose()

@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    
    session_fabric = get_session_fabric()

    async with session_fabric() as session:
        try:
            yield session
            await session.commit()
            logger.debug('Database session committed successfully')
        except Exception as e:
            await session.rollback()
            logger.error('Database session rollback due to error: %s', str(e))
            raise
        finally:
            logger.debug('Database session closed')