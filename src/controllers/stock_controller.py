from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..usecases.stock_transaction import StockTransactionUseCase
from ..domain.models import StockTransaction, StockTransactionType

router = APIRouter(prefix="/api/v1/stocks", tags=["stocks"])

class StockTransactionRequest(BaseModel):
    user_id: UUID
    stock_symbol: str
    quantity: int
    price: float
    transaction_type: StockTransactionType

class StockTransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    stock_symbol: str
    quantity: int
    price: float
    transaction_type: StockTransactionType
    status: str

@router.post("/transactions", response_model=StockTransactionResponse)
async def create_transaction(
    request: StockTransactionRequest,
    use_case: StockTransactionUseCase = Depends()
) -> StockTransactionResponse:
    try:
        transaction = await use_case.execute_transaction(
            user_id=request.user_id,
            stock_symbol=request.stock_symbol,
            quantity=request.quantity,
            price=request.price,
            transaction_type=request.transaction_type
        )
        return StockTransactionResponse(
            id=transaction.id,
            user_id=transaction.user_id,
            stock_symbol=transaction.stock_symbol,
            quantity=transaction.quantity,
            price=transaction.price,
            transaction_type=transaction.transaction_type,
            status=transaction.status
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transactions/{transaction_id}", response_model=StockTransactionResponse)
async def get_transaction(
    transaction_id: UUID,
    use_case: StockTransactionUseCase = Depends()
) -> StockTransactionResponse:
    transaction = await use_case.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return StockTransactionResponse(
        id=transaction.id,
        user_id=transaction.user_id,
        stock_symbol=transaction.stock_symbol,
        quantity=transaction.quantity,
        price=transaction.price,
        transaction_type=transaction.transaction_type,
        status=transaction.status
    )

@router.get("/users/{user_id}/transactions", response_model=List[StockTransactionResponse])
async def get_user_transactions(
    user_id: UUID,
    use_case: StockTransactionUseCase = Depends()
) -> List[StockTransactionResponse]:
    transactions = await use_case.get_user_transactions(user_id)
    return [
        StockTransactionResponse(
            id=t.id,
            user_id=t.user_id,
            stock_symbol=t.stock_symbol,
            quantity=t.quantity,
            price=t.price,
            transaction_type=t.transaction_type,
            status=t.status
        )
        for t in transactions
    ] 