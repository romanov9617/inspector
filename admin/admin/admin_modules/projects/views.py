from rest_framework import viewsets

from admin_modules.projects.models import Project
from admin_modules.projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
