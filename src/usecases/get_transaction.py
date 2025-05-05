from typing import Optional
from uuid import UUID

from kink import inject

from ..domain.transaction import Transaction
from ..domain.repositories import TransactionRepository

@inject
class GetTransaction:
    def __init__(self, transaction_repo: TransactionRepository):
        self._transaction_repo = transaction_repo

    async def execute(self, transaction_id: UUID) -> Optional[Transaction]:
        return await self._transaction_repo.get_by_id(transaction_id) 