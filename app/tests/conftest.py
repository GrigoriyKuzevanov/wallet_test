import asyncio
import uuid
from collections.abc import AsyncGenerator
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app import models
from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app

testing_engine = create_async_engine(settings.asyncpg_test_url.unicode_string())


TestingAsyncSession = async_sessionmaker(
    testing_engine, autoflush=False, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def start_db() -> None:
    async with testing_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await testing_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator:
    async with TestingAsyncSession() as testing_session:
        yield testing_session


@pytest_asyncio.fixture(scope="session")
async def client(start_db) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        async with TestingAsyncSession() as testing_session:
            yield testing_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_V1_STR}"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def test_wallet(session: AsyncSession) -> models.Wallet:
    wallet_data = {
        "id": str(uuid.uuid4()),
        "balance": 1000,
    }

    wallet = models.Wallet(**wallet_data)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)

    return wallet


@pytest_asyncio.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
