from __future__ import annotations

import uuid

from django.db import models
from django.utils import timezone


class UUIDModel(models.Model):
    """
    A model with a UUID-based primary key field.
    """

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


def local_time():
    t = timezone.now()
    loc = timezone.localtime(t)
    return loc


class TimestampModel(models.Model):
    """
    A timestamped fields model.
    """
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=local_time)
    updated_at = models.DateTimeField(default=local_time)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = local_time()
        super().save(*args, **kwargs)
