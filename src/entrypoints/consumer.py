import asyncio
from kink import di
from temporalio.client import Client

from ..consumers.kafka_consumer import KafkaConsumer
from ..consumers.transaction_consumer import TransactionConsumer
from ..config.kafka import cleanup_kafka

async def main():
    # Get dependencies
    kafka_consumer = di[KafkaConsumer]
    workflow_client = di[Client]
    consumer = TransactionConsumer(kafka_consumer, workflow_client)
    
    try:
        # Start consumer
        await consumer.start()
    except KeyboardInterrupt:
        # Stop consumer and cleanup
        await consumer.stop()
        await cleanup_kafka()

if __name__ == "__main__":
    asyncio.run(main()) 