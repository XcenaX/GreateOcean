from storages.backends.s3boto3 import S3Boto3Storage

from greate_ocean.settings import YANDEX_BUCKET_NAME

class ClientDocsStorage(S3Boto3Storage):
    bucket_name = YANDEX_BUCKET_NAME
    file_overwrite = False