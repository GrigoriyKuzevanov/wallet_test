from collections.abc import AsyncGenerator
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app import models
from app.core.config import settings
from app.core.database import engine, get_db
from app.main import app

TestingAsyncSession = async_sessionmaker(
    engine, autoflush=False, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session")
async def session() -> AsyncGenerator:
    async with TestingAsyncSession() as testing_session:
        yield testing_session


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        async with TestingAsyncSession() as testing_session:
            yield testing_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_V1_STR}"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_wallet(session: AsyncSession) -> models.Wallet:
    wallet_data = {
        "id": "0b404911-c9bd-46e6-bbc3-03b90b39b1d5",
        "balance": 1000,
    }

    wallet = models.Wallet(**wallet_data)
    session.add(wallet)
    await session.commit()
    await session.refresh(wallet)

    return wallet
