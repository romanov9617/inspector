from faststream import Logger

from server import broker
from src.adapter.config.config import config
from src.domain.upload_image import ImageUploadEvent


@broker.subscriber("image.uploads.put")
async def handle_upload(event: ImageUploadEvent, logger: Logger):
    if not event.key.startswith(config.image_uploads_key):
        logger.debug(f"Ignored key: {event.key}")
        return

    logger.info(f"Processing upload: {event.key}")
