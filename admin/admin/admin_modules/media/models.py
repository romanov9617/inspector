from django.db import models

from admin.settings import AUTH_USER_MODEL as User
from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel


class ImageStatus(models.TextChoices):
    PROCCESS_PENDING = "process_pending"
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


class UploadStatus(models.TextChoices):
    INIT = "init"
    SUCCESS = "success"
    ERROR = "error"

class UploadSession(UUIDModel,TimestampModel):
    user            = models.ForeignKey(User, on_delete=models.PROTECT)
    filename        = models.CharField(max_length=255)
    expected_size   = models.BigIntegerField()
    sha256          = models.CharField(max_length=64)
    multipart_id    = models.CharField(max_length=255, blank=True, null=True)
    idempotency_key = models.CharField(max_length=255, unique=True)
    status          = models.CharField(max_length=20, choices=UploadStatus, default=UploadStatus.INIT)
    completed_at    = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "upload_session"

    def s3_key(self):
        return f"{self.id}/{self.filename}"


class Image(UUIDModel, TimestampModel):
    session = models.ForeignKey(UploadSession, on_delete=models.PROTECT, null=True)
    file_key = models.CharField(max_length=512, unique=True)
    width_px = models.IntegerField(null=True, blank=True)
    height_px = models.IntegerField(null=True, blank=True)
    original_size = models.BigIntegerField(null=True, blank=True)
    original_checksum = models.CharField(max_length=128, null=True, blank=True)
    is_verified = models.BooleanField(default=False) # is size and checksum are equal to real file in s3?
    status = models.CharField(max_length=50, choices=ImageStatus, default=ImageStatus.PROCCESS_PENDING)

    class Meta:
        db_table = "image"

    def __str__(self) -> str:
        return f"Image {self.file_key}"
