import aioboto3
import aiofiles

from src.domain.file import MinioDownloadConfig


async def download_file_from_minio(config: MinioDownloadConfig) -> None:
    """
    Асинхронно скачивает объект из MinIO по параметрам из Pydantic-модели.
    """
    session = aioboto3.Session()
    async with session.client(
        's3',
        endpoint_url=str(config.endpoint_url),
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
        aws_session_token=config.session_token,
        region_name=config.region_name
    ) as client:
        response = await client.get_object(Bucket=config.bucket, Key=config.key)
        print(len(response["Body"]))
        async with response['Body'] as stream:
            async with aiofiles.open(config.local_path, 'wb') as f:
                while True:
                    chunk = await stream.read(1024 * 1024)
                    if not chunk:
                        break
                    await f.write(chunk)
