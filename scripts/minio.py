import boto3
import boto3.session
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

def upload_file():
    session = boto3.session.Session(
    aws_access_key_id='PLVRRKWC556OVEEWJKM2',
    aws_secret_access_key='J11vKudVNmCt0WJrfR+0IByNXdJ0vZtI3tUbN9xv',
    aws_session_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJQTFZSUktXQzU1Nk9WRUVXSktNMiIsImF1ZCI6ImFkbWluIiwiZXhwIjoxNzQ3Mjc1ODMwLCJpYXQiOjE3NDcyMzI2MzAsImp0aSI6IjFlNGJlYjY3ZDk3ODQwOTFhYWYwOGYxODllNDk4NzRjIiwic3ViIjoidXNlci0xIiwidG9rZW5fdHlwZSI6ImFjY2VzcyJ9.PnThbnhnnJmFdDmE7kO-119L-fOSKdxd9z-4TjjHrIG9gx7jJAGzoleabCtZ-pW_mhrqR57kYgLhjJQJ_kLF8g'
)

# создаём клиент S3, указывая endpoint MinIO
    s3 = session.client(
        's3',
        endpoint_url='http://localhost:9000',
        config=boto3.session.Config(signature_version='s3v4')
    )

    # загружаем файл
    s3.upload_file(
        Filename='test.txt',
        Bucket='inspector',
        Key='uploads/2/test.txt')

# apply_user_policy("1")

upload_file()
