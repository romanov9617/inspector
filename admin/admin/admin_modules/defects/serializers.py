from django.contrib.auth import get_user_model
from rest_framework import serializers

from admin_modules.defects.models import Defect
from admin_modules.defects.models import DefectVersion
from admin_modules.media.serializers import ImageSerializer

User = get_user_model()

class DefectSerializer(serializers.ModelSerializer):

    image = ImageSerializer()

    class Meta:
        model = Defect
        fields = "__all__"


class DefectVersionSerializer(serializers.ModelSerializer):

    defect = DefectSerializer()
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = DefectVersion
        fields = "__all__"
