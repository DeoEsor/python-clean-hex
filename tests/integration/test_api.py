import pytest
from httpx import AsyncClient
from uuid import UUID, uuid4
from fastapi import FastAPI

from src.entrypoints.api import app
from src.domain.models import StockTransaction, StockTransactionType

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_transaction(client):
    user_id = uuid4()
    response = await client.post(
        "/api/v1/stocks/transactions",
        json={
            "user_id": str(user_id),
            "stock_symbol": "AAPL",
            "quantity": 10,
            "price": 150.0,
            "transaction_type": "buy"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert UUID(data["id"])
    assert UUID(data["user_id"]) == user_id
    assert data["stock_symbol"] == "AAPL"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["transaction_type"] == "buy"
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_get_transaction(client):
    # First create a transaction
    user_id = uuid4()
    create_response = await client.post(
        "/api/v1/stocks/transactions",
        json={
            "user_id": str(user_id),
            "stock_symbol": "AAPL",
            "quantity": 10,
            "price": 150.0,
            "transaction_type": "buy"
        }
    )
    transaction_id = create_response.json()["id"]
    
    # Then get it
    response = await client.get(f"/api/v1/stocks/transactions/{transaction_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == transaction_id
    assert UUID(data["user_id"]) == user_id
    assert data["stock_symbol"] == "AAPL"
    assert data["quantity"] == 10
    assert data["price"] == 150.0
    assert data["transaction_type"] == "buy"

@pytest.mark.asyncio
async def test_get_user_transactions(client):
    user_id = uuid4()
    
    # Create multiple transactions
    await client.post(
        "/api/v1/stocks/transactions",
        json={
            "user_id": str(user_id),
            "stock_symbol": "AAPL",
            "quantity": 10,
            "price": 150.0,
            "transaction_type": "buy"
        }
    )
    await client.post(
        "/api/v1/stocks/transactions",
        json={
            "user_id": str(user_id),
            "stock_symbol": "GOOGL",
            "quantity": 5,
            "price": 2800.0,
            "transaction_type": "sell"
        }
    )
    
    # Get all transactions
    response = await client.get(f"/api/v1/stocks/users/{user_id}/transactions")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(UUID(t["user_id"]) == user_id for t in data)
    assert {t["stock_symbol"] for t in data} == {"AAPL", "GOOGL"} 