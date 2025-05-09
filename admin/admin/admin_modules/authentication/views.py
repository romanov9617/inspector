from rest_framework import viewsets

from admin_modules.authentication.models import User
from admin_modules.authentication.serilalizers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
