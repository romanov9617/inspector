import os
from pathlib import Path

from src.adapter.config.config import config
from src.domain.file import MinioDownloadConfig
from src.domain.upload_image import ImageUploadEvent


def image_to_download_config(image: ImageUploadEvent) -> MinioDownloadConfig:
    """
    Конвертирует событие загрузки изображения в конфиг для скачивания из MinIO.
    Берёт первый Record и извлекает оттуда bucket и key.
    """
    record = image.records[0]
    filename = Path("/".join(image.key.split("/")[1:]))
    local_path = os.path.join(config.file.download_dir, filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    endpoint = f"http://{config.minio.host}:{config.minio.port}"

    return MinioDownloadConfig(
        bucket=record.s3.bucket.name,
        key="/".join(image.key.split("/")[1:]),
        local_path=local_path,
        endpoint_url=endpoint,
        access_key_id=config.minio.access_key_id,
        secret_access_key=config.minio.secret_access_key,
        session_token=config.minio.session_token,
        region_name=config.minio.region_name,
    )
