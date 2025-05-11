from rest_framework import viewsets

from admin_modules.defects.models import Defect
from admin_modules.defects.models import DefectVersion
from admin_modules.defects.serializers import DefectSerializer
from admin_modules.defects.serializers import DefectVersionSerializer


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer


class DefectVersionViewSet(viewsets.ModelViewSet):
    queryset = DefectVersion.objects.all()
    serializer_class = DefectVersionSerializer
