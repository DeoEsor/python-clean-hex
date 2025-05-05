import pytest
from uuid import UUID, uuid4
from datetime import datetime

from src.domain.models import StockTransaction, StockTransactionType, StockTransactionStatus, StockPortfolio

def test_stock_transaction_creation():
    user_id = uuid4()
    transaction = StockTransaction(
        user_id=user_id,
        stock_symbol="AAPL",
        quantity=10,
        price=150.0,
        transaction_type=StockTransactionType.BUY
    )
    
    assert isinstance(transaction.id, UUID)
    assert transaction.user_id == user_id
    assert transaction.stock_symbol == "AAPL"
    assert transaction.quantity == 10
    assert transaction.price == 150.0
    assert transaction.transaction_type == StockTransactionType.BUY
    assert transaction.status == StockTransactionStatus.PENDING
    assert isinstance(transaction.created_at, datetime)
    assert isinstance(transaction.updated_at, datetime)

def test_stock_portfolio_creation():
    user_id = uuid4()
    portfolio = StockPortfolio(
        user_id=user_id,
        stock_symbol="AAPL",
        quantity=100,
        average_price=150.0
    )
    
    assert isinstance(portfolio.id, UUID)
    assert portfolio.user_id == user_id
    assert portfolio.stock_symbol == "AAPL"
    assert portfolio.quantity == 100
    assert portfolio.average_price == 150.0
    assert isinstance(portfolio.created_at, datetime)
    assert isinstance(portfolio.updated_at, datetime) 