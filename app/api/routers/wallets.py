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


@router.post("/", response_model=schemas.WalletBase)
async def post_wallet(
    wallet: schemas.WalletCreate, session: AsyncSession = Depends(get_db)
):
    db_wallet = await crud.create_wallet(session=session, wallet=wallet)
    print(db_wallet)
    return db_wallet


@router.get("/{wallet_uuid}", response_model=schemas.WalletBase)
async def get_wallet(wallet_uuid: uuid.UUID, session: AsyncSession = Depends(get_db)):
    db_wallet = await crud.read_wallet_by_uuid(session=session, wallet_uuid=wallet_uuid)

    if not db_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet with given uuid does not exist",
        )

    return db_wallet


@router.put("/{wallet_uuid}/operation", response_model=schemas.WalletBase)
async def update_wallet(
    wallet_uuid: uuid.UUID,
    update_schema: schemas.WalletUpdate,
    session: AsyncSession = Depends(get_db),
):
    db_wallet = await crud.read_wallet_by_uuid(session=session, wallet_uuid=wallet_uuid)

    if not db_wallet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wallet with given uuid does not exist",
        )

    too_low_balance_exc = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Your balance is too low: {db_wallet.balance}",
    )

    db_wallet = await crud.change_balance(
        session=session,
        db_wallet=db_wallet,
        update_data=update_schema,
        too_low_balance_exc=too_low_balance_exc,
    )

    return db_wallet
