from django.db import models

from admin.settings import AUTH_USER_MODEL as User
from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel


class ImageStatus(models.TextChoices):
    PENDING_UPLOAD    = 'pending_upload',    'Ожидает загрузки'
    UPLOADED          = 'uploaded',          'Загружено'
    UPLOAD_ERROR      = 'upload_error',      'Ошибка загрузки'
    PROCESSING        = 'processing',        'В обработке'
    PROCESSED         = 'processed',         'Обработка завершена'
    ANNOTATION_PENDING = 'annotation_pending','Готово к разметке'
    ANNOTATING        = 'annotating',        'В процессе разметки'
    ANNOTATED         = 'annotated',         'Разметка завершена'
    REVIEW_PENDING    = 'review_pending',    'Ждёт верификации'
    REVIEWED          = 'reviewed',          'Верифицировано'
    APPROVED          = 'approved',          'Одобрено'
    REJECTED          = 'rejected',          'Отклонено'
    ARCHIVED          = 'archived',          'Архивировано'
    ERROR             = 'error',             'Ошибка'

class Image(UUIDModel, TimestampModel):
    file_key = models.CharField(max_length=512, unique=True)
    original_filename = models.CharField(max_length=512, blank=True)
    original_size = models.IntegerField(null=True, blank=True)
    original_checksum = models.CharField(max_length=64, null=True, blank=True)
    width_px = models.IntegerField(null=True, blank=True)
    height_px = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=ImageStatus, default=ImageStatus.PENDING_UPLOAD)
    uploader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="uploaded_images"
    )

    class Meta:
        db_table = "image"

    def __str__(self) -> str:
        return f"Image {self.file_key}"
