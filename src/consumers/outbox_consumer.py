import asyncio
from typing import Dict, Any
from uuid import UUID

from temporalio.client import Client
from kink import inject

from ..domain.repositories import OutboxRepository
from ..clients.temporal_workflows import StockTransactionWorkflow

@inject
class OutboxConsumer:
    def __init__(
        self,
        outbox_repo: OutboxRepository,
        temporal_client: Client,
        batch_size: int = 100,
        poll_interval: float = 1.0
    ):
        self._outbox_repo = outbox_repo
        self._temporal_client = temporal_client
        self._batch_size = batch_size
        self._poll_interval = poll_interval
        self._running = False

    async def start(self):
        self._running = True
        while self._running:
            try:
                messages = await self._outbox_repo.get_pending_messages(self._batch_size)
                for message in messages:
                    await self._process_message(message)
            except Exception as e:
                print(f"Error processing messages: {e}")
            await asyncio.sleep(self._poll_interval)

    async def stop(self):
        self._running = False

    async def _process_message(self, message: Dict[str, Any]):
        try:
            if message.topic == "stock_transaction":
                # Start Temporal workflow
                await self._temporal_client.start_workflow(
                    StockTransactionWorkflow.run,
                    message.payload,
                    id=f"stock-transaction-{message.payload['transaction_id']}",
                    task_queue="stock-transactions"
                )
            
            # Mark message as processed
            await self._outbox_repo.mark_as_processed(message.id)
        except Exception as e:
            print(f"Error processing message {message.id}: {e}") 