import uuid
from pydantic import BaseModel


class WalletBase(BaseModel):
    id: uuid.UUID
    balance: int
    
    class Config:
        from_attributes = True
