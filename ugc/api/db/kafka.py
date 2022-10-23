from logging import getLogger
from typing import Optional

from aiokafka import AIOKafkaProducer
from core.config import config
from db.utils import backoff

logger = getLogger(__name__)


class KafkaHandler:
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send(self, topic: str, value: bytes, key: bytes) -> None:
        await self.producer.send_and_wait(topic=topic, value=value, key=key)

    async def stop(self) -> None:
        await self.producer.stop()


kafka_handler: Optional[KafkaHandler] = None


@backoff(logger)
async def get_kafka_handler() -> KafkaHandler:
    kafka_producer = AIOKafkaProducer(bootstrap_servers=config.kafka_uri)
    await kafka_producer.start()
    return KafkaHandler(kafka_producer)
