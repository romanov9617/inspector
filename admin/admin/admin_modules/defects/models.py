import uuid

from admin_modules.authentication.models import User
from admin_modules.media.models import Image
from admin_modules.ml_models.models import ModelEntry
from django.db import models
from django.db.models.fields.json import JSONField


class Defect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="defects")
    class_code = models.SmallIntegerField()
    bbox_x1 = models.FloatField()
    bbox_y1 = models.FloatField()
    bbox_x2 = models.FloatField()
    bbox_y2 = models.FloatField()
    mask_key = models.CharField(max_length=512)
    confidence = models.DecimalField(max_digits=4, decimal_places=3)
    severity = models.DecimalField(max_digits=4, decimal_places=2)
    model = models.ForeignKey(
        ModelEntry, on_delete=models.PROTECT, related_name="defects"
    )
    source = models.CharField(max_length=50, default="model")
    last_version = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Defect {self.id} on image {self.image.id}"


class DefectVersion(models.Model):
    defect = models.ForeignKey(
        Defect, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="defect_versions"
    )
    payload = JSONField()
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("defect", "version"),)
        ordering = ["-version"]

    def __str__(self):
        return f"DefectVersion {self.version} of {self.defect.id}"
