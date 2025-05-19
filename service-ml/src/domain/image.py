from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field


class ImageStatus:
    PROCCESS_PENDING = "process_pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ANNOTATION_PENDING = "annotation_pending"
    ANNOTATING = "annotating"
    ANNOTATED = "annotated"
    REVIEW_PENDING = "review_pending"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    ARCHIVED = "archived"
    ERROR = "error"

class ImageModel(BaseModel):
    id: Optional[UUID] = Field(None, description="UUID изображения")
    user_id: Optional[UUID] = Field(None, description="UUID пользователя")
    file_key: str = Field(..., description="Ключ (путь) файла, уникальный")
    width_px: Optional[int] = Field(None, description="Ширина в пикселях")
    height_px: Optional[int] = Field(None, description="Высота в пикселях")
    status: str = Field(ImageStatus.PROCCESS_PENDING, description="Статус изображения")
    created_at: Optional[datetime] = Field(None, description="Дата создания")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления")
