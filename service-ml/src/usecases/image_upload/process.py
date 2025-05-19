from pathlib import Path
from typing import TYPE_CHECKING

from server import MODEL

if TYPE_CHECKING:
    from src.adapter.storage.postgre.defects.mutator import AsyncpgDefectsMutator
    from src.adapter.storage.postgre.media.mutator import AsyncpgMediaMutator
    from src.domain.defect import DefectModel

class ProcessImage:
    def __init__(
        self,
        image_path: Path,
        media_mutator: "AsyncpgMediaMutator",
        defects_mutator: "AsyncpgDefectsMutator",
    ):
        self.image_path = image_path
        self.media_mutator = media_mutator
        self.defects_mutator = defects_mutator

    async def process(self) -> None:
        # 1. Получить/создать запись Image
        file_key = str(self.image_path)
        image, _ = await self.media_mutator.get_or_create(file_key=file_key)

        # 2. Вызвать модель на изображении
        results = MODEL.predict(str(self.image_path))

        # 3. Для каждого дефекта сохранить через defects_mutator
        for result in results:
            # Обычно result.masks.xy — список numpy-массивов с координатами полигонов
            if getattr(result, "masks", None) is not None and result.masks.xy is not None:
                polygons = result.masks.xy
                for i, polygon in enumerate(polygons):
                    polygon_tile = polygon.tolist()
                    # Если нужен polygon_full — рассчитай (смещение), если не надо — можно = polygon_tile
                    polygon_full = polygon_tile

                    class_code = int(result.boxes.cls[i])
                    confidence = float(result.boxes.conf[i])

                    defect = DefectModel(
                        image_id=image.id,
                        class_code=class_code,
                        polygon_tile=polygon_tile,
                        polygon_full=polygon_full,
                        mask_key=None,
                        confidence=confidence,
                    )
                    await self.defects_mutator.create(defect)
            # Если только bbox:
            else:
                for i, box in enumerate(result.boxes.xyxy):
                    x1, y1, x2, y2 = map(float, box)
                    polygon_tile = [[x1, y1], [x2, y1], [x2, y2], [x1, y2], [x1, y1]]
                    polygon_full = polygon_tile

                    class_code = int(result.boxes.cls[i])
                    confidence = float(result.boxes.conf[i])

                    defect = DefectModel(
                        image_id=image.id,
                        class_code=class_code,
                        polygon_tile=polygon_tile,
                        polygon_full=polygon_full,
                        mask_key=None,
                        confidence=confidence,
                    )
                    await self.defects_mutator.create(defect)
