from django.db import models
from django.db.models.fields.json import JSONField

from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel


class MLModel(UUIDModel, TimestampModel):
    name = models.CharField(max_length=255)
    git_sha = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True)
    training_set = JSONField(default=dict, blank=True)
    metrics = JSONField(default=dict, blank=True)

    class Meta:
        db_table = "ml_model"

    def __str__(self):
        return self.name
