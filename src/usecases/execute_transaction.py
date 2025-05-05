from typing import Optional
from uuid import UUID

from kink import inject

from ..domain.transaction import Transaction, TransactionType
from ..domain.repositories import TransactionRepository
from ..producers.kafka_producer import KafkaProducer

@inject
class ExecuteTransaction:
    def __init__(
        self,
        transaction_repo: TransactionRepository,
        kafka_producer: KafkaProducer
    ):
        self._transaction_repo = transaction_repo
        self._kafka_producer = kafka_producer

    async def execute(
        self,
        user_id: UUID,
        stock_symbol: str,
        quantity: int,
        price: float,
        transaction_type: TransactionType
    ) -> Transaction:
        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            stock_symbol=stock_symbol,
            quantity=quantity,
            price=price,
            transaction_type=transaction_type
        )
        
        # Save transaction
        transaction = await self._transaction_repo.save(transaction)
        
        # Send message to Kafka
        await self._kafka_producer.send_message(
            "transactions",
            {
                "transaction_id": str(transaction.id),
                "user_id": str(user_id),
                "stock_symbol": stock_symbol,
                "quantity": quantity,
                "price": price,
                "type": transaction_type
            }
        )
        
        return transaction 