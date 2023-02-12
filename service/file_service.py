import uuid

import boto3 as boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from loguru import logger

from core.config import settings


class FileService:
    MEDIA_FILE_PREFIX = "media"
    BUCKET_NAME = settings.BUCKET_NAME

    def __init__(self):
        s3_client_config = Config(
            region_name="ap-northeast-2", signature_version="s3v4", retries={"max_attempts": 10, "mode": "standard"}
        )

        self.s3_client = boto3.client("s3",
                                      aws_access_key_id=settings.AWS_ACCESS_KEY,
                                      aws_secret_access_key=settings.AWS_SECRET_KEY,
                                      config=s3_client_config)

    def generate_file_path(self, user_id: str, ext: str):
        return f"/{user_id}/{uuid.uuid4()}.{ext}"

    def generate_content_type_of_image(self, ext: str):
        if ext == "jpg":
            return f"image/jpeg"
        else:
            return f"image/{ext}"

    def get_media_file_upload_url(self, user_id: str, ext: str):

        path = file_service.generate_file_path(user_id=user_id, ext=ext)
        content_type = file_service.generate_content_type_of_image(ext=ext)

        try:
            url = self.s3_client.generate_presigned_url(
                ClientMethod="put_object",
                Params={
                    "Bucket": FileService.BUCKET_NAME,
                    "Key": FileService.MEDIA_FILE_PREFIX + path,
                    "ContentType": content_type
                },
                ExpiresIn=3600
            )
            logger.info("Got presigned URL: %s", url)
        except ClientError:
            logger.exception(
                "Couldn't get a presigned URL for client method '%s'.", "put_object")
            raise
        return url


file_service = FileService()
