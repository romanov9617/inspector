from rest_framework import mixins
from rest_framework import viewsets

from admin_modules.media.models import Image
from admin_modules.media.serializers import ImageSerializer


class ImageViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
