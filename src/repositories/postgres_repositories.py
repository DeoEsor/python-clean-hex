from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from kink import inject

from ..domain.models import StockTransaction, StockPortfolio, OutboxMessage
from ..domain.repositories import (
    StockTransactionRepository,
    StockPortfolioRepository,
    OutboxRepository
)

@inject
class PostgresStockTransactionRepository(StockTransactionRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, transaction: StockTransaction) -> StockTransaction:
        self._session.add(transaction)
        await self._session.commit()
        return transaction

    async def get_by_id(self, transaction_id: UUID) -> Optional[StockTransaction]:
        result = await self._session.execute(
            select(StockTransaction).where(StockTransaction.id == transaction_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UUID) -> List[StockTransaction]:
        result = await self._session.execute(
            select(StockTransaction).where(StockTransaction.user_id == user_id)
        )
        return list(result.scalars().all())

@inject
class PostgresStockPortfolioRepository(StockPortfolioRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, portfolio: StockPortfolio) -> StockPortfolio:
        self._session.add(portfolio)
        await self._session.commit()
        return portfolio

    async def get_by_user_id(self, user_id: UUID) -> List[StockPortfolio]:
        result = await self._session.execute(
            select(StockPortfolio).where(StockPortfolio.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_user_and_symbol(self, user_id: UUID, symbol: str) -> Optional[StockPortfolio]:
        result = await self._session.execute(
            select(StockPortfolio)
            .where(StockPortfolio.user_id == user_id)
            .where(StockPortfolio.stock_symbol == symbol)
        )
        return result.scalar_one_or_none()

@inject
class PostgresOutboxRepository(OutboxRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, message: OutboxMessage) -> OutboxMessage:
        self._session.add(message)
        await self._session.commit()
        return message

    async def get_pending_messages(self, limit: int = 100) -> List[OutboxMessage]:
        result = await self._session.execute(
            select(OutboxMessage)
            .where(OutboxMessage.status == "pending")
            .limit(limit)
        )
        return list(result.scalars().all())

    async def mark_as_processed(self, message_id: UUID) -> None:
        await self._session.execute(
            update(OutboxMessage)
            .where(OutboxMessage.id == message_id)
            .values(status="processed", processed_at=datetime.utcnow())
        )
 