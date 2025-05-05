import json
from typing import Dict, Any
from aiokafka import AIOKafkaProducer
from kink import inject

@inject
class KafkaProducer:
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def send_message(self, topic: str, message: Dict[str, Any]) -> None:
        try:
            value = json.dumps(message)
            await self._producer.send_and_wait(topic, value.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")
            raise 