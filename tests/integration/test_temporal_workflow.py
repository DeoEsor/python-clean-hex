import pytest
from datetime import datetime
from uuid import UUID, uuid4
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

from src.clients.temporal_workflows import StockTransactionWorkflow
from src.domain.models import StockTransaction, StockPortfolio, StockTransactionType
from src.repositories.postgres_repositories import (
    PostgresStockTransactionRepository,
    PostgresStockPortfolioRepository
)

@pytest.mark.asyncio
async def test_stock_transaction_workflow():
    async with await WorkflowEnvironment.start_time_skipping() as env:
        # Create test data
        user_id = uuid4()
        transaction_id = uuid4()
        transaction_data = {
            "transaction_id": str(transaction_id),
            "user_id": str(user_id),
            "stock_symbol": "AAPL",
            "quantity": 10,
            "price": 150.0,
            "type": "buy"
        }
        
        # Create mock repositories
        transaction_repo = AsyncMock()
        portfolio_repo = AsyncMock()
        
        # Mock transaction retrieval
        transaction = StockTransaction(
            id=transaction_id,
            user_id=user_id,
            stock_symbol="AAPL",
            quantity=10,
            price=150.0,
            transaction_type=StockTransactionType.BUY
        )
        transaction_repo.get_by_id.return_value = transaction
        
        # Mock portfolio operations
        portfolio = StockPortfolio(
            user_id=user_id,
            stock_symbol="AAPL",
            quantity=0,
            average_price=0.0
        )
        portfolio_repo.get_by_user_and_symbol.return_value = portfolio
        portfolio_repo.save.return_value = portfolio
        
        # Create worker
        async with Worker(
            env.client,
            task_queue="stock-transactions",
            workflows=[StockTransactionWorkflow],
            activities=[StockTransactionWorkflow.process_transaction]
        ):
            # Start workflow
            handle = await env.client.start_workflow(
                StockTransactionWorkflow.run,
                transaction_data,
                id=f"test-workflow-{transaction_id}",
                task_queue="stock-transactions"
            )
            
            # Wait for workflow to complete
            result = await handle.result()
            
            # Verify workflow result
            assert result["status"] == "completed"
            assert result["transaction_id"] == str(transaction_id)
            
            # Verify transaction was updated
            transaction_repo.save.assert_called_once()
            saved_transaction = transaction_repo.save.call_args[0][0]
            assert saved_transaction.status == "completed"
            
            # Verify portfolio was updated
            portfolio_repo.save.assert_called_once()
            saved_portfolio = portfolio_repo.save.call_args[0][0]
            assert saved_portfolio.quantity == 10
            assert saved_portfolio.average_price == 150.0 