from rest_framework import viewsets

from admin_modules.annotation.models import AnnotationSession
from admin_modules.annotation.serializers import AnnotationSessionSerializer


class AnnotationSessionViewSet(viewsets.ModelViewSet):
    queryset = AnnotationSession.objects.all()
    serializer_class = AnnotationSessionSerializer
