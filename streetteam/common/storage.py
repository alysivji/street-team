from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """Default will be the Chicago Python workspace

    If we ever need to add more, having this extra layer will help
    """

    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = "chicago-python"


class StaticStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    location = "static"
