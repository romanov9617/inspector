import os
import subprocess
import tempfile

from djoser.views import UserViewSet as DjoserUserViewSet
from jinja2 import Template
from rest_framework.response import Response

MC_ALIAS = "local"
TEMPLATE_PATH = "admin/admin_modules/users/templates/policy_template.j2"

MINIO_ROOT_USER = "minioadmin"
MINIO_ROOT_PASSWORD = "minioadmin"

def apply_user_policy(user_id: str) -> str:
    policy_name = f"user-{user_id}"
    print(os.getcwd())

    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())

    rendered = template.render(user_id=user_id)

    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp:
        tmp.write(rendered)
        tmp.flush()
        process = subprocess.run(["mc", "alias", "set", MC_ALIAS, "http://minio:9000", "minioadmin", "minioadmin"], check=True)
        print(process.stderr)

        process = subprocess.run(["mc", "admin", "policy", "create", MC_ALIAS, policy_name, tmp.name], check=True)
        print(process.stderr)
        os.unlink(tmp.name)

    return policy_name

class CustomUserViewSet(DjoserUserViewSet):
    def create(self, request, *args, **kwargs):
        response: Response = super().create(request, *args, **kwargs)
        print(response.data)
        apply_user_policy(response.data["id"])
        # ПОСЛЕ: ещё что-то можете сделать с response.data
        return response
