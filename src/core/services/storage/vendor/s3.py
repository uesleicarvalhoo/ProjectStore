from typing import Union

import boto3
from botocore.exceptions import ClientError

from src.core.config import settings

from .. import Storage

DEFAULT_BUCKET = settings.AWS_S3_BUCKET


class StorageS3(Storage):
    __client = boto3.client("s3", endpoint_url=settings.AWS_S3_URL)

    def upload_file(self, file: Union[str, bytes], key: str, bucket: str = DEFAULT_BUCKET) -> str:
        binary = file

        if isinstance(file, str):
            with open(file, "rb") as f:
                binary = f.read()

        self.__client.put_object(Body=binary, Bucket=bucket, Key=key)

        return key

    def delete_file(self, key: str, bucket: str = DEFAULT_BUCKET) -> None:
        self.__client.delete_object(Bucket=bucket, Key=key)

    def check_file_exists(self, key: str, bucket: str = DEFAULT_BUCKET) -> bool:
        try:
            self.__client.head_object(Bucket=bucket, Key=key)

        except ClientError:
            return False

        else:
            return True
