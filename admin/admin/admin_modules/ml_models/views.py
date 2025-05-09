from rest_framework import viewsets

from admin_modules.ml_models.models import ModelEntry
from admin_modules.ml_models.serilaizers import MLModelSerializer


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = ModelEntry.objects.all()
    serializer_class = MLModelSerializer
