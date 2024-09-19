import pytest
from httpx import AsyncClient

from app import models, schemas


@pytest.mark.asyncio
async def test_get_wallet(client: AsyncClient, test_wallet: models.Wallet):
    response = await client.get(f"/wallets/{test_wallet.id}")

    assert response.status_code == 200

    response_wallet = schemas.WalletBase(**response.json())

    assert response_wallet.id == test_wallet.id
    assert response_wallet.balance == test_wallet.balance
