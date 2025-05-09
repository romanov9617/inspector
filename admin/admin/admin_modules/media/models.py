import uuid

from admin_modules.authentication.models import User
from admin_modules.projects.models import Project
from django.db import models


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="images"
    )
    file_key = models.CharField(max_length=512, unique=True)
    original_filename = models.CharField(max_length=512, blank=True)
    captured_at = models.DateTimeField(null=True, blank=True)
    width_px = models.IntegerField(null=True, blank=True)
    height_px = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50)
    uploader = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="uploaded_images"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image {self.id} of project {self.project.name}"
