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
    aws_access_key_id='5U2R9K7IF93ZLVF8F5CD',
    aws_secret_access_key='JG3DZpZvZ5FG5qpE+pGx1W2WsNxWUgB3HEjUI6y8',
    aws_session_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiI1VTJSOUs3SUY5M1pMVkY4RjVDRCIsImF1ZCI6ImFkbWluIiwiZXhwIjoxNzQ3Mzg0NTQwLCJpYXQiOjE3NDczNDEzNDAsImp0aSI6IjRiMDU3YWZhODZkYzQ3ODJiNmRkYjA2ZjQ0NzNjNDA2Iiwic3ViIjoidXNlci0xNCIsInRva2VuX3R5cGUiOiJhY2Nlc3MifQ.6g4z1VGZIM2Z7gafCxIburvbtKxJK5oOyfhDrRJ4lvHQ18dy4zGFniSVAKsvVSViI3eTgPYKUN8_AfDvf-bIdA'
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
        Key='uploads/14/test.txt')

# apply_user_policy("1")

upload_file()
