from datetime import datetime

import jwt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin.settings import SERVICE_NAME
from admin.settings import SIGNING_KEY
from admin.settings import SIGNING_KID


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):



    def validate(self, attrs):
        data = super().validate(attrs)

        # with open(SERVICE_PRIVATE_KEY, "rb") as f:
        #     private_key = f.read()

        # Пересобираем access token с `kid` в заголовке
        user = self.user
        payload = self.get_token(user)

        custom_payload = {
            "token_type": "access",
            "aud": SERVICE_NAME,
            "exp": datetime.fromtimestamp(payload["exp"]),
            "iat": datetime.fromtimestamp(payload["iat"]),
            "jti": str(payload["jti"]),
            "sub": f"user-{user.pk}",
            "user_id": user.pk
            # "policy": f"user-{user.pk}"
        }

        headers = {"kid": SIGNING_KID}
        access = jwt.encode(
            custom_payload,
            SIGNING_KEY,
            algorithm="RS256",
            headers=headers
        )

        data["access"] = access
        return data
