from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class UserIdentity(BaseModel):
    principal_id: str = Field(..., alias="principalId")


class RequestParameters(BaseModel):
    principal_id: str = Field(..., alias="principalId")
    region: str
    source_ip_address: str = Field(..., alias="sourceIPAddress")


class ResponseElements(BaseModel):
    x_amz_id_2: str = Field(..., alias="x-amz-id-2")
    x_amz_request_id: str = Field(..., alias="x-amz-request-id")
    x_minio_deployment_id: str = Field(..., alias="x-minio-deployment-id")
    x_minio_origin_endpoint: str = Field(..., alias="x-minio-origin-endpoint")


class BucketOwnerIdentity(BaseModel):
    principal_id: str = Field(..., alias="principalId")


class Bucket(BaseModel):
    name: str
    owner_identity: BucketOwnerIdentity = Field(..., alias="ownerIdentity")
    arn: str


class S3ObjectUserMetadata(BaseModel):
    content_type: str = Field(..., alias="content-type")


class S3Object(BaseModel):
    key: str
    size: int
    e_tag: str = Field(..., alias="eTag")
    content_type: str = Field(..., alias="contentType")
    user_metadata: Optional[dict[str, str]] = Field(default=None, alias="userMetadata")
    sequencer: str


class S3(BaseModel):
    s3_schema_version: str = Field(..., alias="s3SchemaVersion")
    configuration_id: str = Field(..., alias="configurationId")
    bucket: Bucket
    object: S3Object


class Source(BaseModel):
    host: str
    port: Optional[str]
    user_agent: str = Field(..., alias="userAgent")


class Record(BaseModel):
    event_version: str = Field(..., alias="eventVersion")
    event_source: str = Field(..., alias="eventSource")
    aws_region: str = Field(..., alias="awsRegion")
    event_time: datetime = Field(..., alias="eventTime")
    event_name: str = Field(..., alias="eventName")
    user_identity: UserIdentity = Field(..., alias="userIdentity")
    request_parameters: RequestParameters = Field(..., alias="requestParameters")
    response_elements: ResponseElements = Field(..., alias="responseElements")
    s3: S3
    source: Source

def alias_gen(s: str) -> str:
    return ''.join(
            part.capitalize() if i else part
            for i, part in enumerate(s.split('_'))
        )

class ImageUploadEvent(BaseModel):
    event_name: str = Field(..., alias="EventName")
    key: str = Field(..., alias="Key")
    records: list[Record] = Field(..., alias="Records")

    class Config:
        allow_population_by_field_name = True
        alias_generator = alias_gen
        allow_population_by_field_name = True
