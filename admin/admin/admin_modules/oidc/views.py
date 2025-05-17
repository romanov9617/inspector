from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from jwcrypto import jwk
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from admin.settings import SERVICE_NAME
from admin.settings import SERVICE_PORT
from admin.settings import SERVICE_PUBLIC_KEY
from admin_modules.oidc.serializers import HealthCheckSerializer
from admin_modules.oidc.serializers import JWKSKeySerializer
from admin_modules.oidc.serializers import OpenIDConfigurationSerializer


class OpenIDConfigurationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=OpenIDConfigurationSerializer, tags=["service"])
    def get(self, request):
        issuer = f"http://{SERVICE_NAME}:{SERVICE_PORT}"
        return JsonResponse({
            "issuer": issuer,
            "jwks_uri": f"{issuer}/jwks.json",
            "id_token_signing_alg_values_supported": ["RS256"]
        })


class JWKSView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=JWKSKeySerializer,tags=["service"])
    def get(self, request):
        with open(SERVICE_PUBLIC_KEY, "rb") as f:
            pub_key = jwk.JWK.from_pem(f.read())
        return JsonResponse({
            "keys": [pub_key.export(as_dict=True)]
        })


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(responses=HealthCheckSerializer, tags=["service"])
    def get(self, request):
        return JsonResponse({"status": "ok"})
