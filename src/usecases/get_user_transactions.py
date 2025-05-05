from typing import List
from uuid import UUID

from kink import inject

from ..domain.transaction import Transaction
from ..domain.repositories import TransactionRepository

@inject
class GetUserTransactions:
    def __init__(self, transaction_repo: TransactionRepository):
        self._transaction_repo = transaction_repo

    async def execute(self, user_id: UUID) -> List[Transaction]:
        return await self._transaction_repo.get_by_user_id(user_id) 