import os
import json
from kafka import KafkaProducer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda m: json.dumps(m).encode()
)


def send_kafka_message(topic: str, message: dict):
    producer.send(topic, message)
    producer.flush()
