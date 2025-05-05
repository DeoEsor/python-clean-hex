from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..portfolio import Portfolio

class PortfolioRepository(ABC):
    @abstractmethod
    async def save(self, portfolio: Portfolio) -> Portfolio:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[Portfolio]:
        pass

    @abstractmethod
    async def get_by_user_and_symbol(self, user_id: UUID, symbol: str) -> Optional[Portfolio]:
        pass 