from django.contrib.auth import get_user_model
from rest_framework import serializers

from admin_modules.media.models import Image

User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Image
        fields = "__all__"


class ImageCreateSerializer(serializers.Serializer):
    file_key = serializers.CharField(max_length=512)
    width_px = serializers.IntegerField(required=False)
    height_px = serializers.IntegerField(required=False)

class CompleteRequestSerializer(serializers.Serializer):
    images = ImageCreateSerializer(many=True)

class STSCredentialsSerializer(serializers.Serializer):
    access_key_id = serializers.CharField()
    secret_access_key = serializers.CharField()
    session_token = serializers.CharField()
    bucket = serializers.CharField()
    key = serializers.CharField()
