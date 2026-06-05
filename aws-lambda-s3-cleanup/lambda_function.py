import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'YOUR_BUCKET_NAME'

def lambda_handler(event, context):

    deleted_files = []

    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if 'Contents' not in response:
        return {
            'statusCode': 200,
            'message': 'Bucket is empty'
        }

    threshold_date = datetime.now(
        timezone.utc
    ) - timedelta(days=30)

    for obj in response['Contents']:

        if obj['LastModified'] < threshold_date:

            s3.delete_object(
                Bucket=BUCKET_NAME,
                Key=obj['Key']
            )

            deleted_files.append(obj['Key'])

            print(f"Deleted: {obj['Key']}")

    return {
        'statusCode': 200,
        'deleted_files': deleted_files
    }
