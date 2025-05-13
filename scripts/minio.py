from jinja2 import Template
import subprocess
import tempfile
import os

MC_ALIAS = "local"
TEMPLATE_PATH = "policy_template.j2"

MINIO_ROOT_USER = "minioadmin"
MINIO_ROOT_PASSWORD = "minioadmin"

def apply_user_policy(user_id: str) -> str:
    policy_name = f"user-{user_id}"
    with open(TEMPLATE_PATH) as f:
        template = Template(f.read())

    rendered = template.render(user_id=user_id)

    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as tmp:
        tmp.write(rendered)
        tmp.flush()
        process = subprocess.run(["mc", "alias", "set", MC_ALIAS, "http://localhost:9000", "minioadmin", "minioadmin"], check=True)
        print(process.stderr)

        process = subprocess.run(["mc", "admin", "policy", "create", MC_ALIAS, policy_name, tmp.name], check=True)
        print(process.stderr)
        os.unlink(tmp.name)

    return policy_name


apply_user_policy("1")
