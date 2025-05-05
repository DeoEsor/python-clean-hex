from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kink import di

from .settings import get_settings

async def init_kafka():
    settings = get_settings()
    
    # Create Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: str(v).encode('utf-8')
    )
    await producer.start()
    
    # Create Kafka consumer
    consumer = AIOKafkaConsumer(
        settings.KAFKA_TRANSACTIONS_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id=settings.KAFKA_CONSUMER_GROUP,
        value_deserializer=lambda v: v.decode('utf-8')
    )
    await consumer.start()
    
    # Register in DI container
    di[AIOKafkaProducer] = producer
    di[AIOKafkaConsumer] = consumer

async def cleanup_kafka():
    # Get instances from DI container
    producer = di[AIOKafkaProducer]
    consumer = di[AIOKafkaConsumer]
    
    # Stop producer and consumer
    await producer.stop()
    await consumer.stop() 