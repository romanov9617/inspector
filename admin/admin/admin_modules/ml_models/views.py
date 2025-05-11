from rest_framework import viewsets

from admin_modules.ml_models.models import MLModel
from admin_modules.ml_models.serilaizers import MLModelSerializer


class MLModelViewSet(viewsets.ModelViewSet):
    queryset = MLModel.objects.all()
    serializer_class = MLModelSerializer
