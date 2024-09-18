from fastapi import FastAPI

from app.api.routers import wallets
from app.core.config import settings

app = FastAPI(title="Wallet-test")


app.include_router(wallets.router, prefix=settings.API_V1_STR)
