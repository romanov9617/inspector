from django.db import models

from admin.settings import AUTH_USER_MODEL as User
from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel


class ReportStatus(models.TextChoices):
    DRAFT = 'DRAFT'
    READY = 'READY'
    GENERATING = 'GENERATING'
    COMPLETED = 'COMPLETED'
    ERROR = 'ERROR'


class Report(UUIDModel, TimestampModel):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports')
    title = models.CharField(max_length=255)
    params = models.JSONField(null=True, blank=True)
    content_json = models.JSONField(null=True, blank=True)
    pdf_key = models.CharField(max_length=512, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.DRAFT,
    )

    class Meta:
        db_table = "report"

    def __str__(self):
        return self.title
