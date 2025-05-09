from rest_framework import viewsets

from admin_modules.media.models import Image
from admin_modules.media.serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
