# src/consumer.py

import logging

from faststream import FastStream
from faststream import Logger
from faststream.kafka import KafkaBroker

from src.domain.upload_image import (
    ImageUploadEvent,  # <- Pydantic-модель из прошлого шага
)

# Настраиваем логирование
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
)

# Создаём брокер и приложение FastStream
broker = KafkaBroker("localhost:9092")
app = FastStream(broker)


@broker.subscriber(
    topic="image.uploads.put",
    group_id="upload-inspector-service",
    # можно указать max_workers для параллельной обработки
    max_workers=4,
    # auto_commit=True по умолчанию,
    # можно настроить offset_reset="earliest" или "latest"
)
async def handle_upload(event: ImageUploadEvent, logger: Logger):
    """
    FastStream автоматически:
      1) десериализует сообщение из JSON,
      2) проверяет его через Pydantic (ImageUploadEvent),
      3) передаёт уже готовый объект event, и
      4) инжектит logger для удобства логирования.
    """
    # фильтруем по нужному префиксу
    if not event.key.startswith("inspector/uploads/"):
        logger.debug(f"Ignored key: {event.key}")
        return

    logger.info(f"Processing upload: {event.key}")

    # доступ к любым данным внутри события напрямую:
    size = event.records[0].s3.object.size
    logger.info(f"Object size: {size} bytes")

    # здесь ваша асинхронная бизнес-логика
    # await process_image(key=event.key, size=size)

    # если нужно — FastStream отправит возвращённый результат в исходящий топик
    # return {"status": "processed", "key": event.key}


if __name__ == "__main__":
    # запускаем loop и подписываемся на Kafka
    app.run()
