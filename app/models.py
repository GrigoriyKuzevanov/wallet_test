import uuid

from sqlalchemy import UUID, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    