# Monitor Unencrypted S3 Buckets Using AWS Lambda and Boto3

## Assignment Objective

The objective of this assignment is to improve AWS security monitoring by detecting Amazon S3 buckets that do not have server-side encryption enabled. AWS Lambda and Boto3 are used to automate the validation of bucket encryption settings.

---

# Services Used

* Amazon S3
* AWS Lambda
* AWS IAM
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Architecture Overview

1. Multiple S3 buckets are created.
2. AWS Lambda retrieves the list of all S3 buckets.
3. Lambda checks the server-side encryption configuration of each bucket.
4. Buckets without encryption are identified and logged.
5. Results are displayed in the Lambda response and CloudWatch logs.

---

# S3 Bucket Setup

Multiple S3 buckets were created for testing.

<img width="2162" height="874" alt="image" src="https://github.com/user-attachments/assets/27a56953-2802-4da9-8456-58da5e3b09ad" />

### Configuration

AWS automatically applies server-side encryption (SSE-S3) to newly created S3 buckets. Therefore, all buckets created during this assignment were encrypted by default.

### Encryption Type

```text
Server-side encryption with Amazon S3 managed keys (SSE-S3)
```

<img width="3238" height="680" alt="image" src="https://github.com/user-attachments/assets/923e8a01-9965-4a18-816c-23d689003f12" />

---

# IAM Role Configuration

A dedicated IAM role was created for the Lambda function.

### Attached Policies

* AmazonS3ReadOnlyAccess
* AWSLambdaBasicExecutionRole

These permissions allow Lambda to:

* List S3 buckets
* Read bucket encryption settings
* Write execution logs to CloudWatch

<img width="2834" height="1344" alt="image" src="https://github.com/user-attachments/assets/cbcb6d90-67c4-4808-b782-67b77e0db692" />

---

# Lambda Function Configuration

| Property      | Value                    |
| ------------- | ------------------------ |
| Function Name | DetectUnencryptedBuckets |
| Runtime       | Python 3.x               |
| Trigger       | Manual Invocation        |
| SDK           | Boto3                    |

<img width="3334" height="844" alt="image" src="https://github.com/user-attachments/assets/7a430695-d3b0-4f71-8103-d1f4cfadbc51" />

---

# Lambda Function Code

```python
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
```

<img width="3188" height="1540" alt="image" src="https://github.com/user-attachments/assets/95eef904-f2dd-402a-b388-e6a6ab2caa66" />

---

# Implementation Steps

## Step 1: Create S3 Buckets

* Opened the AWS S3 Console.
* Created multiple S3 buckets for testing.
* Verified bucket encryption settings.

## Step 2: Create IAM Role

* Opened AWS IAM Console.
* Created a role for Lambda.
* Attached:

  * AmazonS3ReadOnlyAccess
  * AWSLambdaBasicExecutionRole

## Step 3: Create Lambda Function

* Opened AWS Lambda Console.
* Created a Python Lambda function.
* Assigned the IAM role created earlier.

## Step 4: Develop Boto3 Script

The script performs the following operations:

* Connects to Amazon S3.
* Retrieves all bucket names.
* Checks bucket encryption configuration.
* Identifies buckets without server-side encryption.
* Logs non-compliant bucket names.

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
  "unencrypted_buckets": []
}
```

<img width="2330" height="1114" alt="image" src="https://github.com/user-attachments/assets/b4d877dd-500b-41b7-a353-e51e2fa3e953" />

---

# Verification

The Lambda function successfully scanned all available S3 buckets and checked their encryption configuration.

Since AWS now automatically enables server-side encryption (SSE-S3) on newly created S3 buckets, all test buckets were identified as encrypted.

As a result, no unencrypted buckets were detected during execution.

---

# CloudWatch Logs

CloudWatch logs were reviewed to verify the execution results.

Example Log Output:

```text
Unencrypted Buckets: []
```

<img width="3266" height="900" alt="image" src="https://github.com/user-attachments/assets/6e6af7c3-14a9-4938-87a1-4448edd10808" />

---

# Repository Structure

```text
aws-lambda-s3-encryption-monitor/
│
├── lambda_function.py
├── README.md
```

---

# Outcome

The AWS Lambda function successfully monitored the encryption status of Amazon S3 buckets using Boto3. The function validated server-side encryption settings and reported any non-compliant buckets. During testing, all buckets were found to be encrypted because AWS automatically enables SSE-S3 encryption on newly created buckets. This assignment demonstrated the use of AWS Lambda, IAM, S3, CloudWatch, and Boto3 for automated security monitoring in a serverless environment.
