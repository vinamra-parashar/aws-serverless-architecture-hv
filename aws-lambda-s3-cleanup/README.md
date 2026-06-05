# Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## Assignment Objective

The objective of this assignment is to automate the cleanup of old files stored in an Amazon S3 bucket using AWS Lambda and Boto3. The Lambda function identifies objects older than 30 days and deletes them automatically.

---

# Services Used

* Amazon S3
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Architecture Overview

1. Files are uploaded to an S3 bucket.
2. AWS Lambda scans all objects in the bucket.
3. Lambda checks the LastModified date of each object.
4. Objects older than 30 days are identified.
5. Old objects are deleted automatically.
6. Deleted object names are logged in CloudWatch and returned in the Lambda response.

---

# S3 Bucket Setup

A new Amazon S3 bucket was created for storing files.

<img width="3224" height="1028" alt="image" src="https://github.com/user-attachments/assets/4baedd43-435a-4b58-86fb-2e24ea26365e" />

### Bucket Details

| Property    | Value                |
| ----------- | -------------------- |
| Bucket Type | General Purpose      |
| Versioning  | Disabled             |
| Access      | Default AWS Settings |

Multiple files were uploaded to the bucket for testing purposes.

<img width="3280" height="1254" alt="image" src="https://github.com/user-attachments/assets/e83e5236-faba-4e6f-903f-e6ad59976364" />

---

# IAM Role Configuration

A dedicated IAM role was created for the Lambda function.

### Attached Policies

* AmazonS3FullAccess
* AWSLambdaBasicExecutionRole

These permissions allow Lambda to:

* List objects in the bucket
* Delete objects from the bucket
* Access S3 resources
* Write execution logs to CloudWatch

<img width="2834" height="1342" alt="image" src="https://github.com/user-attachments/assets/3ac1a4cc-1349-4afe-9f7d-dd4968cffdae" />

---

# Lambda Function Configuration

| Property      | Value             |
| ------------- | ----------------- |
| Function Name | S3BucketCleanup   |
| Runtime       | Python 3.x        |
| Trigger       | Manual Invocation |
| SDK           | Boto3             |

<img width="3286" height="862" alt="image" src="https://github.com/user-attachments/assets/9f28955d-cf1f-4529-963f-bd336820eb87" />

---

# Lambda Function Code

```python
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
```

<img width="3316" height="1432" alt="image" src="https://github.com/user-attachments/assets/56069158-24f4-4981-86d5-3af20912c41a" />

---

# Implementation Steps

## Step 1: Create S3 Bucket

* Opened AWS S3 Console.
* Created a new S3 bucket.
* Uploaded multiple files into the bucket.

## Step 2: Create IAM Role

* Opened AWS IAM Console.
* Created a new role for Lambda.
* Attached:

  * AmazonS3FullAccess
  * AWSLambdaBasicExecutionRole

## Step 3: Create Lambda Function

* Opened AWS Lambda Console.
* Created a Python Lambda function.
* Assigned the IAM role created earlier.

## Step 4: Develop Boto3 Script

The script performs the following operations:

* Connects to Amazon S3.
* Lists all objects in the bucket.
* Checks the LastModified timestamp of each object.
* Deletes files older than 30 days.
* Logs deleted file names.

## Step 5: Test Lambda Function

* Created a test event using an empty JSON object.
* Invoked the Lambda function manually.
* Verified successful execution.

---

# Test Event

```json
{}
```

---

# Sample Output

```json
{
  "statusCode": 200,
  "deleted_files": [
    "Screenshot 2026-06-05 at 1.52.06 PM.png",
    "Screenshot 2026-06-05 at 3.04.49 PM.png",
    "Screenshot 2026-06-05 at 3.25.44 PM.png"
  ]
}
```

<img width="2014" height="1236" alt="image" src="https://github.com/user-attachments/assets/4166bfc2-9465-478a-926d-3da165134b60" />

---

# Verification

After executing the Lambda function:

* The files older than the configured threshold were deleted.
* The deleted file names were displayed in the Lambda response.
* The S3 bucket was verified to ensure that only eligible files were removed.

---

# Repository Structure

```text
aws-lambda-s3-cleanup/
│
├── lambda_function.py
├── README.md
```

---

# Outcome

The AWS Lambda function successfully automated the cleanup of files stored in Amazon S3. Using Boto3, the function identified objects older than the specified retention period and deleted them automatically. This assignment demonstrated practical implementation of serverless automation using AWS Lambda, IAM, S3, and Python.
