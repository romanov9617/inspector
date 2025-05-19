import json
import os

import asyncpg
from pydantic import BaseModel

from src.adapter.exceptions.config import ConfigFileNotFoundException
from src.adapter.exceptions.config import EnvVarNotDefinedException


class Config(BaseModel):
    kafka: "KafkaConfig"
    minio: "MinioConfig"
    file: "FileDownloadConfig"
    model: "ModelConfig"
    postgres: "PostgresConfig"

class KafkaConfig(BaseModel):
    host: str
    port: int
    image_uploads_key: str = "inspector/uploads/"
    image_uploads_topic: str

class MinioConfig(BaseModel):
    host: str
    port: int
    access_key_id: str
    secret_access_key: str
    session_token: str| None = None
    region_name: str = "us-east-1"

class PostgresConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def dsn(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class ModelConfig(BaseModel):
    path: str

class FileDownloadConfig(BaseModel):
    download_dir: str

CONFIG_PATH = os.environ.get("CONFIG_PATH")

if not CONFIG_PATH:
    raise EnvVarNotDefinedException("CONFIG_PATH")

if not os.path.exists(CONFIG_PATH):
    raise ConfigFileNotFoundException(CONFIG_PATH)

with open(CONFIG_PATH) as f:
    config_json = json.load(f)

config = Config(**config_json)


async def pg_pool_lifespan():
    pool = await asyncpg.create_pool(
        dsn=config.postgres.dsn,
        min_size=2,
        max_size=10,
    )
    try:
        yield pool
    finally:
        await pool.close()
