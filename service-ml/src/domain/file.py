from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import HttpUrl


class MinioDownloadConfig(BaseModel):
    bucket: str = Field(..., description="Имя S3-бакета в MinIO")
    key: str = Field(..., description="Путь к объекту внутри бакета")
    local_path: str = Field(..., description="Локальный путь для сохранения файла")
    endpoint_url: HttpUrl = Field(..., description="URL вашего MinIO (например, 'http://localhost:9000')")
    access_key_id: str = Field(..., description="Access Key ID для доступа к MinIO")
    secret_access_key: str = Field(..., description="Secret Access Key для доступа к MinIO")
    session_token: Optional[str] = Field(None, description="Session Token, если используется STS")
    region_name: Optional[str] = Field('us-east-1', description="Регион S3, по умолчанию 'us-east-1'")
