from rest_framework import serializers

from admin_modules.ml_models.models import ModelEntry


class MLModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelEntry
        fields = "__all__"
