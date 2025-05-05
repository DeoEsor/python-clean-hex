from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from kink import inject

from ....domain.portfolio import Portfolio
from ....domain.repositories import PortfolioRepository

@inject
class SQLPortfolioRepository(PortfolioRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, portfolio: Portfolio) -> Portfolio:
        self._session.add(portfolio)
        await self._session.commit()
        return portfolio

    async def get_by_user_id(self, user_id: UUID) -> List[Portfolio]:
        result = await self._session.execute(
            select(Portfolio).where(Portfolio.user_id == user_id)
        )
        return list(result.scalars().all())

    async def get_by_user_and_symbol(self, user_id: UUID, symbol: str) -> Optional[Portfolio]:
        result = await self._session.execute(
            select(Portfolio)
            .where(Portfolio.user_id == user_id)
            .where(Portfolio.stock_symbol == symbol)
        )
        return result.scalar_one_or_none() 