# Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Assignment Objective

The objective of this assignment is to automate the backup process for Amazon EBS volumes using AWS Lambda and Boto3. The solution creates EBS snapshots automatically and removes snapshots older than a specified retention period to optimize storage usage and reduce costs.

---

# Services Used

* Amazon EC2
* Amazon EBS
* AWS Lambda
* AWS IAM
* Amazon EventBridge (CloudWatch Events)
* Amazon CloudWatch
* Boto3 (AWS SDK for Python)

---

# Architecture Overview

1. An EBS volume is selected for backup.
2. AWS Lambda creates a snapshot of the EBS volume.
3. Snapshots created by Lambda are tagged for identification.
4. Lambda checks existing snapshots created by the automation.
5. Snapshots older than 30 days are deleted.
6. Snapshot creation and deletion details are logged in CloudWatch.

---

# EBS Volume Setup

An existing EBS volume attached to an EC2 instance was selected for backup.

### Volume Information

| Property      | Description               |
| ------------- | ------------------------- |
| Resource Type | Amazon EBS Volume         |
| Source        | Existing EC2 Instance     |
| Purpose       | Automated Snapshot Backup |

The Volume ID was used in the Lambda function configuration.

<img width="3382" height="444" alt="image" src="https://github.com/user-attachments/assets/f504d728-4ceb-4f65-9571-be9c4f0c2532" />

---

# IAM Role Configuration

A dedicated IAM role was created for the Lambda function.

### Attached Policies

* AmazonEC2FullAccess
* AWSLambdaBasicExecutionRole

These permissions allow Lambda to:

* Create EBS snapshots
* List snapshots
* Delete snapshots
* Create resource tags
* Write logs to CloudWatch

<img width="2834" height="1356" alt="image" src="https://github.com/user-attachments/assets/64325740-7aa9-4d47-b6cc-51f3c3dfe302" />

---

# Lambda Function Configuration

| Property      | Value              |
| ------------- | ------------------ |
| Function Name | EBSSnapshotManager |
| Runtime       | Python 3.x         |
| Trigger       | Manual Invocation  |
| SDK           | Boto3              |

<img width="3392" height="876" alt="image" src="https://github.com/user-attachments/assets/feb62914-a455-4d1a-ab93-d09bb631dc5b" />

---

# Lambda Function Code

```python
import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "YOUR_VOLUME_ID"

def lambda_handler(event, context):

    created_snapshot = None
    deleted_snapshots = []

    # Create snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Snapshot"
    )

    created_snapshot = response['SnapshotId']

    # Tag snapshot
    ec2.create_tags(
        Resources=[created_snapshot],
        Tags=[
            {
                'Key': 'CreatedBy',
                'Value': 'LambdaBackup'
            }
        ]
    )

    print(f"Created Snapshot: {created_snapshot}")

    # Find Lambda-created snapshots
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:CreatedBy',
                'Values': ['LambdaBackup']
            }
        ]
    )

    threshold_date = (
        datetime.now(timezone.utc)
        - timedelta(days=30)
    )

    for snapshot in snapshots['Snapshots']:

        if snapshot['StartTime'] < threshold_date:

            snapshot_id = snapshot['SnapshotId']

            ec2.delete_snapshot(
                SnapshotId=snapshot_id
            )

            deleted_snapshots.append(snapshot_id)

            print(
                f"Deleted Snapshot: {snapshot_id}"
            )

    return {
        "statusCode": 200,
        "created_snapshot": created_snapshot,
        "deleted_snapshots": deleted_snapshots
    }
```

<img width="3130" height="1518" alt="image" src="https://github.com/user-attachments/assets/c8a578c6-a165-4d95-af72-92512a5743c8" />

---

# Implementation Steps

## Step 1: Identify EBS Volume

* Opened the EC2 Console.
* Located an existing EBS volume attached to an EC2 instance.
* Noted the Volume ID.

## Step 2: Create IAM Role

* Opened AWS IAM Console.
* Created a role for Lambda.
* Attached:

  * AmazonEC2FullAccess
  * AWSLambdaBasicExecutionRole

## Step 3: Create Lambda Function

* Opened AWS Lambda Console.
* Created a Python Lambda function.
* Assigned the IAM role created earlier.

## Step 4: Develop Boto3 Script

The script performs the following operations:

* Creates a snapshot of the configured EBS volume.
* Tags snapshots created by Lambda.
* Retrieves Lambda-created snapshots.
* Identifies snapshots older than 30 days.
* Deletes expired snapshots.
* Logs snapshot activities.

## Step 5: Test Lambda Function

* Created a test event using an empty JSON object.
* Invoked the Lambda function manually.
* Verified successful snapshot creation.

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
  "created_snapshot": "snap-061d25c62116ef1a5",
  "deleted_snapshots": []
}
```

<img width="2798" height="1236" alt="image" src="https://github.com/user-attachments/assets/578b3ce6-ae4d-4578-ac74-842667916a82" />

---

# Verification

After executing the Lambda function:

* A new EBS snapshot was successfully created.
* The snapshot appeared in the EC2 Snapshots dashboard.
* Snapshot details were visible in the Lambda execution output.
* Cleanup logic was successfully configured to remove snapshots older than the retention period.

<img width="3400" height="458" alt="image" src="https://github.com/user-attachments/assets/5fbfaff5-ae3e-4069-ac65-77a79e852188" />

---

# Bonus: EventBridge Scheduled Trigger

An Amazon EventBridge rule can be configured to automate execution on a schedule.

Example Schedule:

```text
rate(7 days)
```

This allows weekly automated backups without manual intervention.

<img width="3374" height="1538" alt="image" src="https://github.com/user-attachments/assets/7576c53c-3af6-4f04-ba9f-39cc11119701" />

---

# CloudWatch Logs

CloudWatch logs were used to verify successful execution.

Example Log Output:

```text
Created Snapshot: snap-061d25c62116ef1a5
```

---

# Repository Structure

```text
aws-lambda-ebs-snapshot-management/
│
├── lambda_function.py
├── README.md
```

---

# Outcome

The AWS Lambda function successfully automated EBS volume backups using Boto3. The solution created snapshots, tagged them for management, and implemented automated cleanup logic for snapshots older than the configured retention period. This assignment demonstrated the practical use of AWS Lambda, EBS, IAM, EventBridge, CloudWatch, and Boto3 for serverless backup automation and lifecycle management.
