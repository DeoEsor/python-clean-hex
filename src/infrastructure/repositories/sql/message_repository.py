from typing import List
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from kink import inject

from ....domain.message import Message
from ....domain.repositories import MessageRepository

@inject
class SQLMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, message: Message) -> Message:
        self._session.add(message)
        await self._session.commit()
        return message

    async def get_pending_messages(self, limit: int = 100) -> List[Message]:
        result = await self._session.execute(
            select(Message)
            .where(Message.status == "pending")
            .limit(limit)
        )
        return list(result.scalars().all())

    async def mark_as_processed(self, message_id: UUID) -> None:
        await self._session.execute(
            update(Message)
            .where(Message.id == message_id)
            .values(status="processed", processed_at=datetime.utcnow())
        )
        await self._session.commit() 