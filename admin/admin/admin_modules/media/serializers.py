from rest_framework import serializers

from admin_modules.authentication.serilalizers import UserSerializer
from admin_modules.media.models import Image
from admin_modules.projects.serializers import ProjectSerializer


class ImageSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = Image
        fields = "__all__"
