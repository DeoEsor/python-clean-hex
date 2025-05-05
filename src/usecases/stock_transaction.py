from typing import Optional
from uuid import UUID

from kink import inject

from ..domain.models import StockTransaction, StockTransactionType, StockTransactionStatus
from ..domain.repositories import StockTransactionRepository, StockPortfolioRepository, OutboxRepository

@inject
class StockTransactionUseCase:
    def __init__(
        self,
        transaction_repo: StockTransactionRepository,
        portfolio_repo: StockPortfolioRepository,
        outbox_repo: OutboxRepository
    ):
        self._transaction_repo = transaction_repo
        self._portfolio_repo = portfolio_repo
        self._outbox_repo = outbox_repo

    async def execute_transaction(
        self,
        user_id: UUID,
        stock_symbol: str,
        quantity: int,
        price: float,
        transaction_type: StockTransactionType
    ) -> StockTransaction:
        # Create transaction
        transaction = StockTransaction(
            user_id=user_id,
            stock_symbol=stock_symbol,
            quantity=quantity,
            price=price,
            transaction_type=transaction_type
        )
        
        # Save transaction
        transaction = await self._transaction_repo.save(transaction)
        
        # Create outbox message for async processing
        outbox_message = await self._outbox_repo.save(
            OutboxMessage(
                topic="stock_transaction",
                payload={
                    "transaction_id": str(transaction.id),
                    "user_id": str(user_id),
                    "stock_symbol": stock_symbol,
                    "quantity": quantity,
                    "price": price,
                    "type": transaction_type
                }
            )
        )
        
        return transaction

    async def get_transaction(self, transaction_id: UUID) -> Optional[StockTransaction]:
        return await self._transaction_repo.get_by_id(transaction_id)

    async def get_user_transactions(self, user_id: UUID) -> list[StockTransaction]:
        return await self._transaction_repo.get_by_user_id(user_id) 