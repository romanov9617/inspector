from django.db import models
from django.db.models.fields.json import JSONField

from admin.settings import AUTH_USER_MODEL as User
from admin_modules.core.models.mixins import TimestampModel
from admin_modules.core.models.mixins import UUIDModel
from admin_modules.media.models import Image


class Defect(UUIDModel, TimestampModel):
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="defects")
    class_code = models.SmallIntegerField()
    polygon_tile = models.JSONField(help_text="Координаты относительно тайла", null=True)
    polygon_full = models.JSONField(help_text="Координаты относительно всей ленты", null=True)
    mask_key = models.CharField(max_length=512)
    confidence = models.DecimalField(max_digits=4, decimal_places=3)

    class Meta:
        db_table = "defect"

    def __str__(self):
        return f"Defect {self.id} on image {self.image.id}"


class DefectVersion(TimestampModel):
    defect = models.ForeignKey(
        Defect, on_delete=models.CASCADE, related_name="versions"
    )
    version = models.IntegerField()
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="defect_versions"
    )
    payload = JSONField()

    class Meta:
        db_table = "defect_version"
        unique_together = (("defect", "version"),)
        ordering = ["-version"]

    def __str__(self):
        return f"DefectVersion {self.version} of {self.defect.id}"
