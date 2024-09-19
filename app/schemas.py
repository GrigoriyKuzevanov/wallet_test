import uuid
from pydantic import BaseModel
from enum import Enum


class WalletOperationChoices(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class WalletBase(BaseModel):
    id: uuid.UUID
    balance: int
    
    class Config:
        from_attributes = True
        
        
class WalletUpdate(BaseModel):
    operation_type: WalletOperationChoices
    amount: int
