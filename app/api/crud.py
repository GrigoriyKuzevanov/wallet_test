import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas


async def read_wallet_by_uuid(
    session: AsyncSession, wallet_uuid: uuid.UUID
) -> models.Wallet | None:
    wallet = await session.get(models.Wallet, wallet_uuid)
    return wallet
