from rest_framework import mixins
from rest_framework import viewsets

from admin_modules.media.models import Image
from admin_modules.media.serializers import ImageSerializer


class ImageViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


    # @extend_schema(
    #     summary="Инициализация загрузки изображений",
    #     request=InitUploadSerializer,
    #     responses={
    #         201: OpenApiResponse(
    #             description="STS credentials and upload session ID",
    #             response={
    #                 "type": "object",
    #                 "properties": {
    #                     "upload_id": {"type": "string", "format": "uuid"},
    #                     "credentials": {
    #                         "type": "object",
    #                         "properties": {
    #                             "access_key_id": {"type": "string"},
    #                             "secret_access_key": {"type": "string"},
    #                             "session_token": {"type": "string"},
    #                             "expiration": {"type": "string", "format": "date-time"},
    #                             "bucket": {"type": "string"},
    #                             "region": {"type": "string"},
    #                             "keys": {
    #                                 "type": "array",
    #                                 "items": {"type": "string"},
    #                             },
    #                         },
    #                     },
    #                 },
    #             },
    #         )
    #     },
    #     parameters=[
    #         OpenApiParameter(
    #             name="Idempotency-Key",
    #             type=str,
    #             location=OpenApiParameter.HEADER,
    #             required=True,
    #             description="Уникальный ключ запроса для идемпотентности"
    #         )
    #     ],
    #     tags=["media"]
    # )
    # @action(detail=False, methods=['post'], url_path='initiate', permission_classes=[IsAuthenticated])
    # def init_upload(self, request:Request):
    #     serializer = InitUploadSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     files = serializer.validated_data["files"]
    #     filenames = [f["original_filename"] for f in files]
    #     idem_key = request.headers.get("Idempotency-Key")
    #     user = request.user

    #     session, _ = UploadSession.objects.get_or_create(
    #         idempotency_key=idem_key,
    #         defaults={"user": user}
    #     )

    #     for f in files:
    #         file_key = f"{session.id}/{f['original_filename']}"
    #         Image.objects.get_or_create(
    #             session=session,
    #             file_key=file_key,
    #             defaults={
    #                 "original_size": f["original_size"],
    #                 "original_checksum": f["original_checksum"],
    #                 "status": ImageStatus.PROCCESS_PENDING,
    #             }
    #         )

    #     creds = get_or_create_upload_credentials(
    #         user_id=str(user.id),
    #         idem_key=idem_key,
    #         upload_id=str(session.id),
    #         filenames=filenames
    #     )

    #     return response.Response({
    #         "upload_id": session.id,
    #         "credentials": creds
    #     }, status=201)

    # @extend_schema(
    #     summary="Завершение загрузки изображений",
    #     responses={
    #         200: OpenApiResponse(
    #             description="Список успешно загруженных и ошибочных файлов",
    #             response={
    #                 "type": "object",
    #                 "properties": {
    #                     "completed": {
    #                         "type": "array",
    #                         "items": {"type": "string"}
    #                     },
    #                     "errors": {
    #                         "type": "array",
    #                         "items": {
    #                             "type": "object",
    #                             "properties": {
    #                                 "file_key": {"type": "string"},
    #                                 "error": {"type": "string"}
    #                             }
    #                         }
    #                     }
    #                 }
    #             }
    #         )
    #     },
    #     tags=["media"]
    # )
    # @action(detail=True, methods=["post"], url_path="complete", permission_classes=[IsAuthenticated])
    # def complete_upload(self, request, pk=None):
    #     session = get_object_or_404(UploadSession, id=pk, user=request.user)
    #     s3 = S3s.s3_client()
    #     bucket = AWS_STORAGE_BUCKET_NAME

    #     errors = []
    #     updated_images = []

    #     for image in session.image_set.all():
    #         try:
    #             meta = s3.head_object(Bucket=bucket, Key=image.file_key)
    #         except Exception as e:
    #             errors.append({"file_key": image.file_key, "error": str(e)})
    #             continue

    #         size = meta["ContentLength"]
    #         image.uploaded_size = size

    #         if image.expected_size and image.expected_size != size:
    #             image.status = ImageStatus.UPLOAD_FAILED
    #             image.verified = False
    #             errors.append({"file_key": image.file_key, "error": "Size mismatch"})
    #         else:
    #             image.status = ImageStatus.PROCCESS_PENDING  # или READY
    #             image.verified = True

    #         image.save()
    #         updated_images.append(image.file_key)

    #     session.status = "completed"
    #     session.save()

    #     return response.Response({
    #         "completed": updated_images,
    #         "errors": errors
    #     }, status=200)
