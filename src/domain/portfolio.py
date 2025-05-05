from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Portfolio(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    stock_symbol: str
    quantity: int
    average_price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow) 