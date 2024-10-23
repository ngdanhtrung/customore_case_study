import boto3
import logging

from os.path import splitext
from botocore.exceptions import ClientError

from delivery.configs.settings import (
    S3_ENDPOINT_URL,
    S3_PORT,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
)
from delivery.utils.common import get_utcnow_int


aws_credentials = {
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    "endpoint_url": f"{S3_ENDPOINT_URL}:{S3_PORT}",
}

s3r = boto3.resource("s3", **aws_credentials)
s3c = boto3.client("s3", **aws_credentials)


def upload_file_to_s3(file, pre_key, use_utcnow: bool = True, name: str = None):
    # file name from utc now
    file_name = name or file.name
    if use_utcnow:
        file_name = f"{get_utcnow_int()}{splitext(file.name)[1].lower()}"
    file_key = f"{pre_key}/{file_name}"

    s3_uploaded_url = s3r.Bucket("delivery").put_object(
        Key=file_key, Body=file, ContentType=file.content_type
    )
    return s3_uploaded_url.key


def downloadFileFromS3(file_key):
    s3_object = s3c.get_object(Bucket="delivery", Key=file_key)
    return s3_object["Body"].read()


def deleteFileFromS3(file_key):
    s3r.Object("delivery", file_key).delete()


def putObject2S3(key, file):
    s3r.Object("delivery", key).put(Body=file)


def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    # s3_client = boto3.client("s3")
    try:
        response = s3c.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def delete_s3_folder(folder_path: str):
    try:
        s3r.Bucket("delivery").objects.filter(Prefix=folder_path).delete()
    except Exception as e:
        logging.error(f"Error while deleting folder {folder_path}: {e}")
        return False
    return True


def upload_object_to_s3(buffer, pre_key, use_utcnow=True, name: str = None):
    file_name = name
    if use_utcnow:
        file_name = f"{get_utcnow_int()}{splitext(name)[1].lower()}"

    file_key = f"{pre_key}/{file_name}"
    s3_uploaded_url = s3c.upload_fileobj(buffer, "delivery", file_key)
    return file_key
