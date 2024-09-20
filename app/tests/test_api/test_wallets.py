import random
import uuid

import pytest
from httpx import AsyncClient

from app import models, schemas


@pytest.mark.asyncio
async def test_post_wallet(client: AsyncClient) -> None:
    post_data = {
        "balance": 1000,
    }
    response = await client.post("/wallets/", json=post_data)

    assert response.status_code == 200

    wallet = schemas.WalletBase(**response.json())

    assert wallet.balance == post_data.get("balance")


@pytest.mark.asyncio
async def test_get_wallet(client: AsyncClient, test_wallet: models.Wallet) -> None:
    response = await client.get(f"/wallets/{test_wallet.id}")

    assert response.status_code == 200

    response_wallet = schemas.WalletBase(**response.json())

    assert response_wallet.id == test_wallet.id
    assert response_wallet.balance == test_wallet.balance


@pytest.mark.asyncio
async def test_update_wallet_deposit(
    client: AsyncClient, test_wallet: models.Wallet
) -> None:
    random_amount = random.randint(1, 10000)
    deposit_data = {
        "operationType": "DEPOSIT",
        "amount": random_amount,
    }

    response = await client.put(
        f"/wallets/{test_wallet.id}/operation", json=deposit_data
    )

    assert response.status_code == 200

    response_wallet = schemas.WalletBase(**response.json())

    assert response_wallet.id == test_wallet.id
    assert response_wallet.balance == test_wallet.balance + random_amount


@pytest.mark.asyncio
async def test_update_wallet_withdraw(
    client: AsyncClient, test_wallet: models.Wallet
) -> None:
    random_amount = random.randint(1, 1000)
    deposit_data = {
        "operationType": "WITHDRAW",
        "amount": random_amount,
    }

    response = await client.put(
        f"/wallets/{test_wallet.id}/operation", json=deposit_data
    )

    assert response.status_code == 200

    response_wallet = schemas.WalletBase(**response.json())

    assert response_wallet.id == test_wallet.id
    assert response_wallet.balance == test_wallet.balance - random_amount


@pytest.mark.asyncio
async def test_update_wallet_withdraw_too_low_balance(
    client: AsyncClient, test_wallet: models.Wallet
) -> None:
    too_big_amount = test_wallet.balance + 1
    deposit_data = {
        "operationType": "WITHDRAW",
        "amount": too_big_amount,
    }

    response = await client.put(
        f"/wallets/{test_wallet.id}/operation", json=deposit_data
    )

    assert response.status_code == 400
    assert (
        response.json().get("detail")
        == f"Your balance is too low: {test_wallet.balance}"
    )


@pytest.mark.asyncio
async def test_update_wallet_not_exists(client: AsyncClient) -> None:
    random_uuid = str(uuid.uuid4())
    deposit_data = {
        "operationType": "DEPOSIT",
        "amount": 100,
    }

    response = await client.put(f"/wallets/{random_uuid}/operation", json=deposit_data)

    assert response.status_code == 404
    assert response.json().get("detail") == "Wallet with given uuid does not exist"
