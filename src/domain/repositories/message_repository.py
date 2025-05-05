from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ..message import Message

class MessageRepository(ABC):
    @abstractmethod
    async def save(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def get_pending_messages(self, limit: int = 100) -> List[Message]:
        pass

    @abstractmethod
    async def mark_as_processed(self, message_id: UUID) -> None:
        pass 