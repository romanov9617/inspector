from django.http import JsonResponse
from jwcrypto import jwk
from rest_framework.decorators import api_view


@api_view(['GET'])
def openid_configuration(request):
    issuer = "http://host.docker.internal:8000"  # или домен, где работает твой Django
    return JsonResponse({
        "issuer": issuer,
        "jwks_uri": f"{issuer}/jwks.json",
        "id_token_signing_alg_values_supported": ["RS256"]
    })

@api_view(['GET'])
def jwks(request):
    with open("./.certs/public.key", "rb") as f:
        pub_key = jwk.JWK.from_pem(f.read())
    jwks = {"keys": [pub_key.export(as_dict=True)]}
    return JsonResponse(jwks)
