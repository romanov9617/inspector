# project/container.py
import boto3
from dependency_injector import containers
from dependency_injector import providers


class S3s(containers.DeclarativeContainer):
    """Контейнер для настроек и провайдера S3-клиента"""
    config = providers.Configuration()

    # Singleton-провайдер boto3.client('s3', **credentials)
    s3_client = providers.Singleton( # type: ignore
        boto3.client,
        service_name='s3',
        region_name=config.region_name,
        aws_access_key_id=config.access_key_id,
        aws_secret_access_key=config.secret_access_key,
    )
