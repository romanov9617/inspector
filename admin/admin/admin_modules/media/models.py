from django.db import models

from admin.settings import AUTH_USER_MODEL as User
from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel


class ImageStatus(models.TextChoices):
    PROCCESS_PENDING = "process_pending", "Готово к обработке"
    PROCESSING = "processing", "В обработке"
    PROCESSED = "processed", "Обработка завершена"
    ANNOTATION_PENDING = "annotation_pending", "Готово к разметке"
    ANNOTATING = "annotating", "В процессе разметки"
    ANNOTATED = "annotated", "Разметка завершена"
    REVIEW_PENDING = "review_pending", "Ждёт верификации"
    REVIEWED = "reviewed", "Верифицировано"
    APPROVED = "approved", "Одобрено"
    REJECTED = "rejected", "Отклонено"
    ARCHIVED = "archived", "Архивировано"
    ERROR = "error", "Ошибка"


class Image(UUIDModel, TimestampModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    file_key = models.CharField(max_length=512, unique=True)
    width_px = models.IntegerField(null=True, blank=True)
    height_px = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=ImageStatus, default=ImageStatus.PROCCESS_PENDING
    )

    class Meta:
        db_table = "image"

    def __str__(self) -> str:
        return f"Image {self.file_key}"
