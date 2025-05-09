from rest_framework import viewsets

from admin_modules.defects.models import Defect
from admin_modules.defects.serializers import DefectSerializer


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
