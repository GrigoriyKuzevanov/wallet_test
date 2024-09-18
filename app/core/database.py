from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    settings.asyncpg_url.unicode_string(), echo=settings.ECHO_SQL
)


AsyncSessionFactory = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
