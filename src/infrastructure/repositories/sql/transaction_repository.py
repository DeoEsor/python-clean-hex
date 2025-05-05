from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from kink import inject

from ....domain.transaction import Transaction
from ....domain.repositories import TransactionRepository

@inject
class SQLTransactionRepository(TransactionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, transaction: Transaction) -> Transaction:
        self._session.add(transaction)
        await self._session.commit()
        return transaction

    async def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        result = await self._session.execute(
            select(Transaction).where(Transaction.id == transaction_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> List[Transaction]:
        result = await self._session.execute(
            select(Transaction).where(Transaction.user_id == user_id)
        )
        return list(result.scalars().all()) 