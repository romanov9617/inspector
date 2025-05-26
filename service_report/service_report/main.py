
import os
import json
import logging
from kafka import KafkaConsumer
from usecases.report_service import (handle_processing_completed,
                                     handle_reports_pdf)

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("report-service")

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")

consumer = KafkaConsumer(
    "processing.completed",
    "reports.pdf",
    bootstrap_servers=BOOTSTRAP,
    group_id="report-service",
    value_deserializer=lambda m: json.loads(m.decode()),
    auto_offset_reset="earliest"
)

if __name__ == "__main__":
    LOG.info("report-service started")
    for msg in consumer:
        try:
            if msg.topic == "processing.completed":
                handle_processing_completed(msg.value)
            elif msg.topic == "reports.pdf":
                handle_reports_pdf(msg.value)
        except Exception as e:
            LOG.exception("Error handling topic %s: %s", msg.topic, e)
