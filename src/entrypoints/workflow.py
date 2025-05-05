import asyncio
from temporalio.worker import Worker
from kink import di

from ..infrastructure.workflow.transaction_workflow import TransactionWorkflow

async def main():
    # Get workflow client
    client = di[Client]
    
    # Create worker
    async with Worker(
        client,
        task_queue="transactions",
        workflows=[TransactionWorkflow],
        activities=[TransactionWorkflow.process_transaction]
    ):
        # Run worker
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main()) 