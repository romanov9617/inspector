import logging

from faststream.kafka import KafkaBroker

from src.adapter.config.config import config

broker = KafkaBroker(f"{config.kafka.host}:{config.kafka.port}")

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)

logging.info("broker configured")
