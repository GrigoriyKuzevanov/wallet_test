import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def read_wallet_by_uuid(
    session: AsyncSession, wallet_uuid: uuid.UUID
) -> models.Wallet | None:
    wallet = await session.get(models.Wallet, wallet_uuid)

    return wallet


async def deposit_wallet(
    session: AsyncSession, db_wallet: models.Wallet, amount: int
) -> models.Wallet:
    db_wallet.balance += amount
    print(db_wallet.balance)
    await session.commit()
    await session.refresh(db_wallet)

    return db_wallet


async def withdraw_wallet(
    session: AsyncSession, db_wallet: models.Wallet, amount: int
) -> models.Wallet:
    db_wallet.balance -= amount
    await session.commit()
    await session.refresh(db_wallet)

    return db_wallet
