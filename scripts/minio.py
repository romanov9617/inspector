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
    aws_access_key_id='0KTUAGH314R6V2C2ZA97',
    aws_secret_access_key='Am0qawHwKx3Byxg0OVzwbhxHgbBs1b8vVtSZawpd',
    aws_session_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiIwS1RVQUdIMzE0UjZWMkMyWkE5NyIsImF1ZCI6ImFkbWluIiwiZXhwIjoxNzQ3NDY5MzY4LCJpYXQiOjE3NDc0MjYxNjgsImp0aSI6Ijg5ZDg2ZjE4ZjA1MjQ1ZTliMDY3ZDFlYjc0OGRhN2IzIiwic3ViIjoidXNlci00IiwidG9rZW5fdHlwZSI6ImFjY2VzcyIsInVzZXJfaWQiOjR9.cDRMYpLumQCmblpzUSgt4byfWq1QO74bGHHoCPyWADrByZNlWIEfB83tnnNuvV3KYm7QoCur20du9Mzyf_S6oQ'
)

# создаём клиент S3, указывая endpoint MinIO
    s3 = session.client(
        's3',
        endpoint_url='http://localhost:9000',
        config=boto3.session.Config(signature_version='s3v4')
    )

    # загружаем файл
    s3.upload_file(
        Filename='0-250-ls-r1-1-23nv.png',
        Bucket='inspector',
        Key='uploads/4/0-250-ls-r1-1-23nv.png')

# apply_user_policy("1")

upload_file()
