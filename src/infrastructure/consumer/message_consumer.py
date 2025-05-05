import asyncio
from typing import Dict, Any
from uuid import UUID

from temporalio.client import Client
from kink import inject

from ..messaging.kafka_service import KafkaService
from ..workflow.transaction_workflow import TransactionWorkflow

@inject
class MessageConsumer:
    def __init__(
        self,
        kafka_service: KafkaService,
        workflow_client: Client
    ):
        self._kafka_service = kafka_service
        self._workflow_client = workflow_client
        self._running = False

    async def start(self):
        self._running = True
        await self._kafka_service.consume_messages(self._process_message)

    async def stop(self):
        self._running = False

    async def _process_message(self, message: Dict[str, Any]):
        try:
            # Start workflow
            await self._workflow_client.start_workflow(
                TransactionWorkflow.run,
                message,
                id=f"transaction-{message['transaction_id']}",
                task_queue="transactions"
            )
        except Exception as e:
            print(f"Error processing message: {e}") 