from rest_framework import serializers

from admin_modules.authentication.serilalizers import UserSerializer
from admin_modules.defects.models import Defect
from admin_modules.defects.models import DefectVersion
from admin_modules.media.serializers import ImageSerializer
from admin_modules.ml_models.serilaizers import MLModelSerializer


class DefectSerializer(serializers.ModelSerializer):

    image = ImageSerializer()
    model = MLModelSerializer()

    class Meta:
        model = Defect
        fields = "__all__"


class DefectVersionSerializer(serializers.ModelSerializer):

    defect = DefectSerializer()
    author = UserSerializer()

    class Meta:
        model = DefectVersion
        fields = "__all__"
