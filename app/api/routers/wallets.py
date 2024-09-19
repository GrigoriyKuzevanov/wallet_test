import uuid

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.api import crud
from app.core.database import get_db

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"],
)


@router.get("/{wallet_uuid}", response_model=schemas.WalletBase)
async def get_wallet(wallet_uuid: uuid.UUID, session: AsyncSession = Depends(get_db)):
    db_wallet = await crud.read_wallet_by_uuid(session=session, wallet_uuid=wallet_uuid)

    if not db_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet with given uuid doen not exist",
        )

    return db_wallet
