import json
from datetime import datetime
from datetime import timezone
from uuid import UUID
from uuid import uuid4

import asyncpg

from src.domain.defect import DefectModel
from src.interfaces.postgre.defects.mutator import IDefectsMutator


class AsyncpgDefectsMutator(IDefectsMutator):
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def create(self, defect: DefectModel) -> UUID:
        query = """
            INSERT INTO defect (
                id, image_id, class_code,
                polygon_tile, polygon_full, mask_key, confidence,
                model_id, created_at, updated_at
            )
            VALUES (
                $1, $2, $3, $4::jsonb, $5::jsonb, $6, $7, $8, $9, $10
            )
            RETURNING id
        """
        now = datetime.now(timezone.utc)
        new_id = uuid4()
        # asyncpg работает с UUID, не обязательно приводить к str!
        values = (
            new_id,
            defect.image_id,
            defect.class_code,
            json.dumps(defect.polygon_tile),
            json.dumps(defect.polygon_full),
            defect.mask_key,
            defect.confidence,
            defect.model_id,
            now,
            now,
        )
        async with self.pool.acquire() as conn:
            row: asyncpg.Record = await conn.fetchrow(query, *values)
            return row["id"]
