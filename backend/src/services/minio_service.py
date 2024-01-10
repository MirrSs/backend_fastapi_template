from botocore.exceptions import ClientError
from fastapi import status
from loguru import logger
from utils import check_user_image_extension
from minio import Minio
from minio.error import S3Error
from settings import MINIO_USER_IMAGE_BUCKET_NAME, MINIO_ACCESS_KEY,MINIO_SECRET_KEY

class MinioService:

    client = Minio("minio:9000",
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=False
    )

    @classmethod
    def create_s3_bucket(cls, bucket_name: str, region: str = None) -> bool:
        """Create AWS S3 bucket"""
        try:
            location = {'LocationConstraint': region}
            cls.client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
        except ClientError as err:
            logger.error(err)
            return False
        return True

    @classmethod
    def get_all_s3_buckets(cls) -> list:
        """Return all existing AWS S3 buckets"""
        response = cls.client.list_buckets()
        response_list = []
        for bucket in response['Buckets']:
            response_list.append(f'{bucket["Name"]}')
        return response_list

    @classmethod
    def upload_file(cls, file, object_name: str = None) -> tuple[dict[str, str], int]:
        """Upload a file to an S3 bucket

        :param file: File to upload
        :param bucket: Defines bucket name
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """

        # Make the bucket if it doesn't exist.
        found = cls.client.bucket_exists(MINIO_USER_IMAGE_BUCKET_NAME)
        if not found:
            cls.client.make_bucket(MINIO_USER_IMAGE_BUCKET_NAME)
            print("Created bucket", MINIO_USER_IMAGE_BUCKET_NAME)
        else:
            print("Bucket", MINIO_USER_IMAGE_BUCKET_NAME, "already exists")

        # Upload the file, renaming it in the process
        cls.client.put_object(
            MINIO_USER_IMAGE_BUCKET_NAME,
            object_name,
            file.file,
            length=file.size
        )

        msg = f"FILE {file.filename} successfully uploaded as {object_name}"
        status_code = status.HTTP_201_CREATED
        return msg, status_code

    @classmethod
    def create_presigned_url(cls, object_name: str) -> str:
        """Generate a presigned URL to share an S3 object

        :param object_name: string
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = cls.client.presigned_get_object(
                        'default-bucket',
                        object_name=object_name,
                    )
        except ClientError as err:
            logger.error(err)
            return ''
        return response
