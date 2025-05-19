from datetime import datetime
from datetime import timezone
from typing import Optional
from uuid import UUID
from uuid import uuid4

import asyncpg

from src.domain.image import ImageModel
from src.domain.image import ImageStatus
from src.interfaces.postgre.media.mutator import IMediaMutator


class AsyncpgMediaMutator(IMediaMutator):
    async def get_or_create(
        self,
        pool: asyncpg.Pool,
        file_key: str,
        user_id: Optional[UUID] = None,
        status: str = ImageStatus.PROCCESS_PENDING,
    ) -> tuple[ImageModel, bool]:
        """
        Получить или создать запись Image по file_key.
        Всегда width_px=None, height_px=None при создании.
        Возвращает (ImageModel, created: bool)
        """
        async with pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM image WHERE file_key = $1", file_key
            )
            if row:
                image = ImageModel(
                    id=row["id"],
                    user_id=row["user_id"],
                    file_key=row["file_key"],
                    width_px=row["width_px"],
                    height_px=row["height_px"],
                    status=row["status"],
                    created_at=row["created_at"],
                    updated_at=row["updated_at"],
                )
                return image, False

            now = datetime.now(timezone.utc)
            new_id = uuid4()
            await conn.execute(
                """
                INSERT INTO image (
                    id, user_id, file_key, width_px, height_px, status, created_at, updated_at
                ) VALUES (
                    $1, $2, $3, $4, $5, $6, $7, $8
                )
                """,
                new_id,
                user_id,
                file_key,
                None,  # width_px
                None,  # height_px
                status,
                now,
                now,
            )
            image = ImageModel(
                id=new_id,
                user_id=user_id,
                file_key=file_key,
                width_px=None,
                height_px=None,
                status=status,
                created_at=now,
                updated_at=now,
            )
            return image, True
