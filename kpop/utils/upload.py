from datetime import datetime

import boto3
from django.conf import settings


def generate_presigned_url(filename: str, content_type: str, expires_in=3600):
    s3_client = boto3.client(
        "s3",
        region_name=settings.AWS_S3_REGION_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    date = datetime.today()
    str_date = date.strftime("%Y%m%d%H%M%S")

    # 저장 경로
    key = f"uploads/img/{str_date}_{filename}"

    url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
            "Key": key,
            "ContentType": content_type
        },
        ExpiresIn=expires_in,
    )

    return {
        "upload_url": url,
        "file_url": f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{key}"
    }
