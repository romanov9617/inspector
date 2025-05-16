from faststream import Logger

from server import broker
from src.adapter.config.config import config
from src.adapter.storage.minio.download import download_file_from_minio
from src.domain.upload_image import ImageUploadEvent
from src.usecases.image_upload.converter import image_to_download_config


@broker.subscriber(config.kafka.image_uploads_topic,
                   group_id="upload-inspector-service",
                   max_workers=4,)
async def handle_upload(event: ImageUploadEvent, logger: Logger):
    logger.info(event)
    if not event.key.startswith(config.kafka.image_uploads_key):
        logger.debug(f"Ignored key: {event.key}")
        return
    logger.info(f"Processing upload: {event.key}")
    download_config = image_to_download_config(event)
    logger.info(download_config)
    await download_file_from_minio(download_config)
    return
