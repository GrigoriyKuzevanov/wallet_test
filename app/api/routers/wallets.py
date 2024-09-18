from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app import models

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
)


@router.get("/")
async def get_wallet(session: AsyncSession = Depends(get_db)):
    stmt = select(models.Wallet)
    result = await session.execute(stmt)
    wallets = result.scalars().all()
    return {"wallets": wallets}
