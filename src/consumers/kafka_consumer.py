import json
from typing import Dict, Any, Callable, Awaitable
from aiokafka import AIOKafkaConsumer
from kink import inject

@inject
class KafkaConsumer:
    def __init__(self, consumer: AIOKafkaConsumer):
        self._consumer = consumer

    async def consume_messages(self, handler: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        try:
            async for msg in self._consumer:
                try:
                    value = json.loads(msg.value)
                    await handler(value)
                except json.JSONDecodeError:
                    print(f"Error decoding message: {msg.value}")
                except Exception as e:
                    print(f"Error handling message: {e}")
        except Exception as e:
            print(f"Error consuming messages: {e}")
            raise 