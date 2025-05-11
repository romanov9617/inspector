from django.contrib.auth import get_user_model
from rest_framework import serializers

from admin_modules.reports.models import Report

User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):

    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Report
        fields = "__all__"
