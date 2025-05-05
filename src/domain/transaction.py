from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class TransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Transaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    stock_symbol: str
    quantity: int
    price: float
    transaction_type: TransactionType
    status: TransactionStatus = TransactionStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 