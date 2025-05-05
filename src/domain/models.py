from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class StockTransactionType(str, Enum):
    BUY = "buy"
    SELL = "sell"

class StockTransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StockTransaction(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    stock_symbol: str
    quantity: int
    price: float
    transaction_type: StockTransactionType
    status: StockTransactionStatus = StockTransactionStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class StockPortfolio(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    stock_symbol: str
    quantity: int
    average_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class OutboxMessage(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    topic: str
    payload: dict
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None 