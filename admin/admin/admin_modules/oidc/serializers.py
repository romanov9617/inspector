# serializers.py
from rest_framework import serializers


class OpenIDConfigurationSerializer(serializers.Serializer):
    issuer = serializers.CharField()
    jwks_uri = serializers.CharField()
    id_token_signing_alg_values_supported = serializers.ListField(
        child=serializers.CharField()
    )

class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()

class JWKSKeySerializer(serializers.Serializer):
    kty = serializers.CharField()
    n = serializers.CharField()
    e = serializers.CharField()
    kid = serializers.CharField(required=False)

class JWKSResponseSerializer(serializers.Serializer):
    keys = JWKSKeySerializer(many=True)
