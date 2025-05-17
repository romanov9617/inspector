import requests  # type: ignore
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from admin.settings import AWS_HOST
from admin.settings import AWS_PORT
from admin.settings import AWS_STORAGE_BUCKET_NAME
from admin_modules.media.models import Image
from admin_modules.media.models import ImageStatus
from admin_modules.media.serializers import CompleteRequestSerializer
from admin_modules.media.serializers import ImageSerializer
from admin_modules.media.serializers import STSCredentialsSerializer
from admin_modules.media.utils import parse_sts_credentials


class ImageViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()

    @extend_schema(
        request=None,  # нет тела
        responses={200: STSCredentialsSerializer},
        description="Проксирует запрос к MinIO STS: AssumeRoleWithWebIdentity",
    )
    @action(detail=False, methods=["get"], url_path="initiate")
    def initiate(self, request: Request):
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth.startswith("Bearer "):
            return Response(
                {"detail": "Missing or invalid Authorization header"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        web_identity_token = auth.split(" ", 1)[1]

        # Собираем параметры для STS-запроса
        params = {
            "Action": "AssumeRoleWithWebIdentity",
            "Version": "2011-06-15",
            "WebIdentityToken": web_identity_token,
        }
        try:
            resp = requests.post(
                f"http://{AWS_HOST}:{AWS_PORT}", params=params, timeout=5
            )
            resp.raise_for_status()
            creds_data = parse_sts_credentials(resp.content)
        except requests.RequestException as e:
            return Response(
                {"detail": f"Error talking to STS: {e}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        creds_data["bucket"] = AWS_STORAGE_BUCKET_NAME
        creds_data["key"] = f"uploads/{request.user.pk}/"
        serializer = STSCredentialsSerializer(data=creds_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CompleteRequestSerializer,
        responses={200: ImageSerializer(many=True)},
        description='Финализирует сессию загрузки и создаёт объекты Image'
    )
    @action(detail=False, methods=['post'], url_path='complete')
    def complete(self, request: Request):
        images = request.data.get("images", [])
        if not images:
            return Response({"detail": "images required"}, status=400)
        created = []
        for image_data in images:
            img = Image.objects.create(
                user=request.user,
                file_key=image_data["file_key"],
                width_px=image_data.get("width_px"),
                height_px=image_data.get("height_px"),
                status=ImageStatus.PROCCESS_PENDING
            )
            created.append(img)
        return Response(ImageSerializer(created, many=True).data, status=200)
