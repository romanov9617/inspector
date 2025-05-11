from rest_framework import viewsets

from admin_modules.reports.models import Report
from admin_modules.reports.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
