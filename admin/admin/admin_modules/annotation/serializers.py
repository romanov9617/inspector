from rest_framework import serializers

from admin_modules.annotation.models import AnnotationSession
from admin_modules.authentication.serilalizers import UserSerializer
from admin_modules.media.serializers import ImageSerializer


class AnnotationSessionSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    image = ImageSerializer()

    class Meta:
        model = AnnotationSession
        fields = "__all__"
