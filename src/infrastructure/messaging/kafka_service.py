import json
from typing import Dict, Any
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from kink import inject

@inject
class KafkaService:
    def __init__(
        self,
        producer: AIOKafkaProducer,
        consumer: AIOKafkaConsumer
    ):
        self._producer = producer
        self._consumer = consumer

    async def send_message(self, topic: str, message: Dict[str, Any]) -> None:
        """Send a message to a Kafka topic."""
        try:
            # Convert message to JSON string
            value = json.dumps(message)
            # Send message
            await self._producer.send_and_wait(topic, value.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")
            raise

    async def consume_messages(self, handler) -> None:
        """Consume messages from subscribed topics."""
        try:
            async for msg in self._consumer:
                try:
                    # Parse message value
                    value = json.loads(msg.value)
                    # Handle message
                    await handler(value)
                except json.JSONDecodeError:
                    print(f"Error decoding message: {msg.value}")
                except Exception as e:
                    print(f"Error handling message: {e}")
        except Exception as e:
            print(f"Error consuming messages: {e}")
            raise 