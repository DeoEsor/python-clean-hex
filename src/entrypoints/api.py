from fastapi import FastAPI
from kink import di

from ..controllers.transaction_controller import router as transaction_router
from ..infrastructure.repositories.sql import (
    SQLTransactionRepository,
    SQLPortfolioRepository,
    SQLMessageRepository
)
from ..usecases import ExecuteTransaction, GetTransaction, GetUserTransactions

app = FastAPI(title="Stock Service", version="1.0.0")

# Register routes
app.include_router(transaction_router)

# Setup dependency injection
@di.factory
def provide_execute_transaction() -> ExecuteTransaction:
    return ExecuteTransaction(
        transaction_repo=di[SQLTransactionRepository],
        portfolio_repo=di[SQLPortfolioRepository],
        message_repo=di[SQLMessageRepository]
    )

@di.factory
def provide_get_transaction() -> GetTransaction:
    return GetTransaction(transaction_repo=di[SQLTransactionRepository])

@di.factory
def provide_get_user_transactions() -> GetUserTransactions:
    return GetUserTransactions(transaction_repo=di[SQLTransactionRepository]) 