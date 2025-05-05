from datetime import timedelta
from typing import Dict, Any
from uuid import UUID

from temporalio import workflow
from temporalio.common import RetryPolicy

from ..domain.models import StockTransactionStatus
from ..domain.repositories import StockTransactionRepository, StockPortfolioRepository

@workflow.defn
class StockTransactionWorkflow:
    def __init__(self):
        self._transaction_id: UUID = None
        self._status: StockTransactionStatus = StockTransactionStatus.PENDING

    @workflow.run
    async def run(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        self._transaction_id = UUID(transaction_data["transaction_id"])
        
        # Start transaction processing
        await workflow.execute_activity(
            self.process_transaction,
            transaction_data,
            start_to_close_timeout=timedelta(minutes=5),
            retry_policy=RetryPolicy(
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(minutes=1),
                maximum_attempts=3
            )
        )
        
        return {"status": "completed", "transaction_id": str(self._transaction_id)}

    @workflow.activity
    async def process_transaction(
        self,
        transaction_data: Dict[str, Any],
        transaction_repo: StockTransactionRepository,
        portfolio_repo: StockPortfolioRepository
    ) -> None:
        # Get transaction
        transaction = await transaction_repo.get_by_id(self._transaction_id)
        if not transaction:
            raise ValueError(f"Transaction {self._transaction_id} not found")

        # Update portfolio based on transaction
        portfolio = await portfolio_repo.get_by_user_and_symbol(
            transaction.user_id,
            transaction.stock_symbol
        )

        if transaction.transaction_type == "buy":
            if portfolio:
                # Update existing portfolio
                portfolio.quantity += transaction.quantity
                portfolio.average_price = (
                    (portfolio.average_price * portfolio.quantity + 
                     transaction.price * transaction.quantity) /
                    (portfolio.quantity + transaction.quantity)
                )
            else:
                # Create new portfolio
                portfolio = StockPortfolio(
                    user_id=transaction.user_id,
                    stock_symbol=transaction.stock_symbol,
                    quantity=transaction.quantity,
                    average_price=transaction.price
                )
        else:  # sell
            if not portfolio or portfolio.quantity < transaction.quantity:
                raise ValueError("Insufficient stock quantity")
            portfolio.quantity -= transaction.quantity

        # Save changes
        await portfolio_repo.save(portfolio)
        transaction.status = StockTransactionStatus.COMPLETED
        await transaction_repo.save(transaction) 