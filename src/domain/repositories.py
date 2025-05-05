from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from .models import StockTransaction, StockPortfolio, OutboxMessage

class StockTransactionRepository(ABC):
    @abstractmethod
    async def save(self, transaction: StockTransaction) -> StockTransaction:
        pass

    @abstractmethod
    async def get_by_id(self, transaction_id: UUID) -> Optional[StockTransaction]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[StockTransaction]:
        pass

class StockPortfolioRepository(ABC):
    @abstractmethod
    async def save(self, portfolio: StockPortfolio) -> StockPortfolio:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> List[StockPortfolio]:
        pass

    @abstractmethod
    async def get_by_user_and_symbol(self, user_id: UUID, symbol: str) -> Optional[StockPortfolio]:
        pass

class OutboxRepository(ABC):
    @abstractmethod
    async def save(self, message: OutboxMessage) -> OutboxMessage:
        pass

    @abstractmethod
    async def get_pending_messages(self, limit: int = 100) -> List[OutboxMessage]:
        pass

    @abstractmethod
    async def mark_as_processed(self, message_id: UUID) -> None:
        pass 