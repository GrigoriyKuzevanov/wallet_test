import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def create_wallet(
    session: AsyncSession, wallet: schemas.WalletCreate
) -> models.Wallet:
    db_wallet = models.Wallet(**wallet.model_dump())

    session.add(db_wallet)
    await session.commit()
    await session.refresh(db_wallet)

    return db_wallet


async def read_wallet_by_uuid(
    session: AsyncSession, wallet_uuid: uuid.UUID
) -> models.Wallet | None:
    wallet = await session.get(models.Wallet, wallet_uuid)

    return wallet


async def deposit_wallet(
    session: AsyncSession, db_wallet: models.Wallet, amount: int
) -> models.Wallet:
    db_wallet.balance += amount
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


async def change_balance(
    session: AsyncSession,
    db_wallet: models.Wallet,
    update_data: schemas.WalletUpdate,
    too_low_balance_exc: Exception,
) -> models.Wallet:
    if update_data.operationType.name == "DEPOSIT":
        db_wallet.balance += update_data.amount

    if update_data.operationType.name == "WITHDRAW":
        db_wallet.balance -= update_data.amount

        if db_wallet.balance < 0:
            raise too_low_balance_exc

    await session.commit()
    await session.refresh(db_wallet)

    return db_wallet
