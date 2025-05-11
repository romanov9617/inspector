from django.contrib.auth import get_user_model
from rest_framework import serializers

from admin_modules.media.models import Image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):

    uploader = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Image
        fields = "__all__"


class ImageInitUploadSerializer(serializers.Serializer):

    original_filename = serializers.CharField(max_length=255)
    original_size = serializers.IntegerField()
    original_checksum = serializers.CharField(max_length=64)

class InitUploadSerializer(serializers.Serializer):

    files = ImageInitUploadSerializer(many=True)
