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
    # Если нужно поддерживать несколько записей, можно итерировать по image.records
    record = image.records[0]

    # Директория для сохранения загруженных файлов
    download_dir = os.getenv("DOWNLOAD_DIR", "/tmp/")
    filename = Path("/".join(image.key.split("/")[1:]))
    local_path = os.path.join(download_dir, filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    endpoint = os.getenv("MINIO_ENDPOINT_URL", "http://minio:9000")

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
