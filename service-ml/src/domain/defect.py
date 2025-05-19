from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field


class DefectCreate(BaseModel):
    image_id: UUID = Field(..., description="UUID изображения-тайла")
    class_code: int = Field(..., description="Код класса дефекта")
    polygon_tile: list[list[float]] = Field(..., description="Координаты полигона относительно тайла")
    polygon_full: list[list[float]] = Field(..., description="Координаты полигона относительно всей ленты")
    mask_key: Optional[str] = Field(None, description="Ключ к маске, если есть")
    confidence: float = Field(..., ge=0, le=1, description="Уверенность детекции")

class DefectModel(BaseModel):
    id: Optional[UUID] = Field(None, description="UUID дефекта")
    image_id: UUID = Field(..., description="UUID изображения-тайла")
    class_code: int = Field(..., description="Код класса дефекта")
    polygon_tile: list[list[float]] = Field(..., description="Координаты полигона относительно тайла")
    polygon_full: list[list[float]] = Field(..., description="Координаты полигона относительно всей ленты")
    mask_key: Optional[str] = Field(None, description="Ключ к маске, если есть")
    confidence: float = Field(..., ge=0, le=1, description="Уверенность детекции")
    created_at: Optional[datetime] = Field(None, description="Когда создано")
    updated_at: Optional[datetime] = Field(None, description="Когда обновлено")
