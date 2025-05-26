import json
import os

from pydantic import BaseModel

from src.adapter.exceptions.config import ConfigFileNotFoundException
from src.adapter.exceptions.config import EnvVarNotDefinedException


class Config(BaseModel):
    kafka: "KafkaConfig"
    minio: "MinioConfig"
    file: "FileDownloadConfig"

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
