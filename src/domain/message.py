from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Message(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    topic: str
    payload: dict
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processed_at: Optional[datetime] = None 