import boto3
from botocore.exceptions import ClientError

s3 = boto3.client('s3')


def lambda_handler(event, context):

    unencrypted_buckets = []

    buckets = s3.list_buckets()

    for bucket in buckets['Buckets']:

        bucket_name = bucket['Name']

        try:
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )

        except ClientError:
            unencrypted_buckets.append(
                bucket_name
            )

    print(
        "Unencrypted Buckets:",
        unencrypted_buckets
    )

    return {
        "statusCode": 200,
        "unencrypted_buckets":
            unencrypted_buckets
    }
