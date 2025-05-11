# uploads/services.py
import json
from datetime import timedelta

from admin.container import RedisContainer
from admin.container import S3s
from admin.settings import AWS_S3_REGION_NAME
from admin.settings import AWS_STORAGE_BUCKET_NAME


def get_or_create_upload_credentials(user_id: str, idem_key: str, upload_id: str, filenames: list[str]):
    redis_key = f"upload-creds:{user_id}:{idem_key}"
    redis_client = RedisContainer.redis_client()
    # пробуем взять из кеша
    cached = redis_client.get(redis_key)
    if cached:
        return json.loads(cached)

    # иначе создаём креды
    bucket = AWS_STORAGE_BUCKET_NAME
    region = AWS_S3_REGION_NAME
    role_arn = S3s.upload_role_arn()
    sts = S3s.sts_client()

    statements = [
        {
            "Effect": "Allow",
            "Action": ["s3:PutObject", "s3:PutObjectAcl", "s3:HeadObject"],
            "Resource": f"arn:aws:s3:::{bucket}/{upload_id}/{filename}"
        }
        for filename in filenames
    ]

    policy = {
        "Version": "2012-10-17",
        "Statement": statements
    }

    resp = sts.assume_role(
        RoleArn=role_arn,
        RoleSessionName=f"upload-{upload_id}",
        DurationSeconds=3600,
        Policy=json.dumps(policy)
    )
    creds = resp["Credentials"]

    payload = {
        "access_key_id": creds["AccessKeyId"],
        "secret_access_key": creds["SecretAccessKey"],
        "session_token": creds["SessionToken"],
        "expiration": creds["Expiration"].isoformat(),
        "bucket": bucket,
        "region": region,
        "keys": [f"{upload_id}/{f}" for f in filenames]
    }

    # сохраним в Redis на 1 час
    redis_client.setex(redis_key, timedelta(hours=1), json.dumps(payload))
    return payload
