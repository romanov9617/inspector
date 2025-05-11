from rest_framework import serializers

from admin_modules.ml_models.models import MLModel


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MLModel
        fields = "__all__"
