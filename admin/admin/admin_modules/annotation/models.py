import uuid

from admin_modules.authentication.models import User
from admin_modules.media.models import Image
from django.db import models


class AnnotationSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="annotation_sessions"
    )
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, related_name="annotation_sessions"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="in_progress")

    def __str__(self):
        return f"Session {self.id} by {self.user.email}"
