import os
from pathlib import Path

from faststream import Logger

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
    Path(download_dir).mkdir(parents=True, exist_ok=True)
    # Имя локального файла — берём имя объекта
    filename = Path(record.s3.object.key).name
    local_path = os.path.join(download_dir, filename)
    Logger.info(local_path)
    # Собираем HttpUrl из строки
    endpoint = os.getenv("MINIO_ENDPOINT_URL", "http://minio:9000")

    return MinioDownloadConfig(
        bucket=record.s3.bucket.name,
        key=record.s3.object.key,
        local_path=local_path,
        endpoint_url=endpoint,
        access_key_id=config.minio.access_key_id,
        secret_access_key=config.minio.secret_access_key,
        session_token=config.minio.session_token,
        region_name=config.minio.region_name,
    )
