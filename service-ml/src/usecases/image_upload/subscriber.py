import asyncpg
from faststream import Depends
from faststream import Logger

from server import broker
from src.adapter.config.config import config
from src.adapter.config.config import pg_pool_lifespan
from src.adapter.storage.minio.download import download_file_from_minio
from src.adapter.storage.postgre.defects.mutator import AsyncpgDefectsMutator
from src.adapter.storage.postgre.media.mutator import AsyncpgMediaMutator
from src.domain.upload_image import ImageUploadEvent
from src.usecases.image_upload.converter import image_to_download_config
from src.usecases.image_upload.process import ProcessImage


@broker.subscriber(
    config.kafka.image_uploads_topic,
    group_id="upload-inspector-service",
    max_workers=4,
)
async def handle_upload(
    event: ImageUploadEvent,
    logger: Logger,
    pool: asyncpg.Pool = Depends(pg_pool_lifespan),
):
    if not event.key.startswith(config.kafka.image_uploads_key):
        logger.debug(f"Ignored key: {event.key}")
        return
    logger.info(f"Processing upload: {event.key}")
    download_config = image_to_download_config(event)
    logger.info(download_config)
    path = await download_file_from_minio(download_config)
    defects_mutator = AsyncpgDefectsMutator(pool)
    media_mutator = AsyncpgMediaMutator(pool)
    process = ProcessImage(path, media_mutator, defects_mutator)
    await process.process()
