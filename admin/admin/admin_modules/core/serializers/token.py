from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin.settings import SIGNING_KID


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['kid'] = SIGNING_KID
        # ...

        return token
