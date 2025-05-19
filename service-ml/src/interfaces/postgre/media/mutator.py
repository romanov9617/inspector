from abc import ABC
from abc import abstractmethod
from typing import Optional
from uuid import UUID

import asyncpg

from src.domain.image import ImageModel
from src.domain.image import ImageStatus


class IMediaMutator(ABC):
    @abstractmethod
    async def get_or_create(
        self,
        pool: asyncpg.Pool,
        file_key: str,
        user_id: Optional[UUID] = None,
        status: str = ImageStatus.PROCCESS_PENDING,
    ) -> tuple[ImageModel, bool]:
        pass
