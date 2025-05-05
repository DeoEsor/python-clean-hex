import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

from src.domain.models import StockTransaction, StockTransactionType, StockTransactionStatus
from src.usecases.stock_transaction import StockTransactionUseCase

@pytest.fixture
def mock_repositories():
    transaction_repo = AsyncMock()
    portfolio_repo = AsyncMock()
    outbox_repo = AsyncMock()
    return transaction_repo, portfolio_repo, outbox_repo

@pytest.fixture
def use_case(mock_repositories):
    transaction_repo, portfolio_repo, outbox_repo = mock_repositories
    return StockTransactionUseCase(transaction_repo, portfolio_repo, outbox_repo)

@pytest.mark.asyncio
async def test_execute_transaction(use_case, mock_repositories):
    transaction_repo, portfolio_repo, outbox_repo = mock_repositories
    
    # Mock transaction save
    saved_transaction = StockTransaction(
        user_id=uuid4(),
        stock_symbol="AAPL",
        quantity=10,
        price=150.0,
        transaction_type=StockTransactionType.BUY
    )
    transaction_repo.save.return_value = saved_transaction
    
    # Mock outbox save
    outbox_repo.save.return_value = MagicMock()
    
    # Execute transaction
    result = await use_case.execute_transaction(
        user_id=saved_transaction.user_id,
        stock_symbol="AAPL",
        quantity=10,
        price=150.0,
        transaction_type=StockTransactionType.BUY
    )
    
    # Verify transaction was saved
    transaction_repo.save.assert_called_once()
    assert isinstance(transaction_repo.save.call_args[0][0], StockTransaction)
    
    # Verify outbox message was created
    outbox_repo.save.assert_called_once()
    outbox_message = outbox_repo.save.call_args[0][0]
    assert outbox_message.topic == "stock_transaction"
    assert outbox_message.payload["stock_symbol"] == "AAPL"
    
    # Verify result
    assert result == saved_transaction

@pytest.mark.asyncio
async def test_get_transaction(use_case, mock_repositories):
    transaction_repo, _, _ = mock_repositories
    
    # Mock transaction retrieval
    transaction_id = uuid4()
    expected_transaction = StockTransaction(
        id=transaction_id,
        user_id=uuid4(),
        stock_symbol="AAPL",
        quantity=10,
        price=150.0,
        transaction_type=StockTransactionType.BUY
    )
    transaction_repo.get_by_id.return_value = expected_transaction
    
    # Get transaction
    result = await use_case.get_transaction(transaction_id)
    
    # Verify transaction was retrieved
    transaction_repo.get_by_id.assert_called_once_with(transaction_id)
    assert result == expected_transaction

@pytest.mark.asyncio
async def test_get_user_transactions(use_case, mock_repositories):
    transaction_repo, _, _ = mock_repositories
    
    # Mock transactions retrieval
    user_id = uuid4()
    expected_transactions = [
        StockTransaction(
            user_id=user_id,
            stock_symbol="AAPL",
            quantity=10,
            price=150.0,
            transaction_type=StockTransactionType.BUY
        ),
        StockTransaction(
            user_id=user_id,
            stock_symbol="GOOGL",
            quantity=5,
            price=2800.0,
            transaction_type=StockTransactionType.SELL
        )
    ]
    transaction_repo.get_by_user_id.return_value = expected_transactions
    
    # Get user transactions
    result = await use_case.get_user_transactions(user_id)
    
    # Verify transactions were retrieved
    transaction_repo.get_by_user_id.assert_called_once_with(user_id)
    assert result == expected_transactions 