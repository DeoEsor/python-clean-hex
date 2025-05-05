import asyncio
from kink import di

from ..infrastructure.repositories.sql import SQLMessageRepository
from ..infrastructure.workflow.transaction_workflow import TransactionWorkflow
from ..infrastructure.consumer.message_consumer import MessageConsumer

async def main():
    # Get dependencies
    message_repo = di[SQLMessageRepository]
    workflow_client = di[Client]
    consumer = MessageConsumer(message_repo, workflow_client)
    
    try:
        # Start consumer
        await consumer.start()
    except KeyboardInterrupt:
        # Stop consumer on interrupt
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(main()) 