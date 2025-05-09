import uuid

from django.db import models
from django.db.models.fields.json import JSONField


class ModelEntry(models.Model):  # renamed to avoid clash with django.db.models.Model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    git_sha = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True)
    training_set = JSONField(default=dict, blank=True)
    metrics = JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
