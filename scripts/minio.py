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
    aws_access_key_id='W0OLMI73S3BDO5JG08QI',
    aws_secret_access_key='V8VfPnp9GTV19JlFs+79NkXxuNHQBi8eXojqJjXJ',
    aws_session_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJXME9MTUk3M1MzQkRPNUpHMDhRSSIsImF1ZCI6ImFkbWluIiwiZXhwIjoxNzQ3NDM3MDM0LCJpYXQiOjE3NDczOTM4MzQsImp0aSI6IjNiOGEwMzgzMWEzMzRkYmI5MzA0YTkyNjUxMWU1NzRmIiwic3ViIjoidXNlci0zIiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsInVzZXJfaWQiOjN9.mdNkc7cB-uyDV4QpUXF78tA1IGylMldfP1HAjOr1BWW1jVcHOVeg--Mkh2mGPqMfcS6JLmKD9L8cgs0n-jy2Wg'
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
        Key='uploads/3/test.txt')

# apply_user_policy("1")

upload_file()
