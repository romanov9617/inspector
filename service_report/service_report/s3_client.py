import os
import boto3

S3_BUCKET = os.environ["S3_BUCKET"]

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://minio:9000"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "1"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "secret"),
)


def upload_pdf_to_s3(file_path, key):
    s3.upload_file(str(file_path), S3_BUCKET, key)
