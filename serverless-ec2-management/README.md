# Automated Instance Management Using AWS Lambda and Boto3

## Assignment Objective

The objective of this assignment is to automate the management of Amazon EC2 instances using AWS Lambda and Boto3. The Lambda function automatically starts or stops EC2 instances based on predefined tags.

---

## Architecture Overview

AWS Services Used:

* Amazon EC2
* AWS Lambda
* AWS IAM
* Boto3 (AWS SDK for Python)

Workflow:

1. Two EC2 instances are created.
2. One instance is tagged with `Action = Auto-Stop`.
3. Another instance is tagged with `Action = Auto-Start`.
4. AWS Lambda scans EC2 instances based on tags.
5. Instances tagged `Auto-Stop` are stopped.
6. Instances tagged `Auto-Start` are started.
7. Lambda execution logs and affected instance IDs are displayed in the output.

---

## EC2 Instance Setup

### Instance 1

| Property      | Value           |
| ------------- | --------------- |
| Name          | Serverless-Stop |
| Instance Type | t3.micro        |
| Tag Key       | Action          |
| Tag Value     | Auto-Stop       |

### Instance 2

| Property      | Value            |
| ------------- | ---------------- |
| Name          | Serverless-Start |
| Instance Type | t3.micro         |
| Tag Key       | Action           |
| Tag Value     | Auto-Start       |

<img width="2960" height="612" alt="image" src="https://github.com/user-attachments/assets/6644802d-7b53-4eb8-90d5-46cf1d2409b2" />

---

## IAM Role Configuration

A dedicated IAM role was created for the Lambda function.

### Attached Policies

* AmazonEC2FullAccess
* AWSLambdaBasicExecutionRole

These permissions allow Lambda to:

* Describe EC2 instances
* Start EC2 instances
* Stop EC2 instances
* Write logs to CloudWatch

<img width="2812" height="1336" alt="image" src="https://github.com/user-attachments/assets/bbebd3ba-b3e0-428b-82f1-45a3e04b5f9b" />

---

## Lambda Function Configuration

| Property      | Value              |
| ------------- | ------------------ |
| Function Name | ManageEC2Instances |
| Runtime       | Python 3.x         |
| Trigger       | Manual Invocation  |
| SDK           | Boto3              |

---

## Lambda Function Code

```python
import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):

    # Find Auto-Stop instances
    stop_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Stop']
            }
        ]
    )

    stop_ids = []

    for reservation in stop_instances['Reservations']:
        for instance in reservation['Instances']:
            stop_ids.append(instance['InstanceId'])

    if stop_ids:
        ec2.stop_instances(InstanceIds=stop_ids)
        print("Stopped Instances:", stop_ids)

    # Find Auto-Start instances
    start_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Action',
                'Values': ['Auto-Start']
            }
        ]
    )

    start_ids = []

    for reservation in start_instances['Reservations']:
        for instance in reservation['Instances']:
            start_ids.append(instance['InstanceId'])

    if start_ids:
        ec2.start_instances(InstanceIds=start_ids)
        print("Started Instances:", start_ids)

    return {
        "statusCode": 200,
        "stopped": stop_ids,
        "started": start_ids
    }
```
<img width="3368" height="1638" alt="image" src="https://github.com/user-attachments/assets/94a89a7a-4978-4fe5-8042-d6a0bf773db7" />
---

## Testing Procedure

### Step 1

Created a Lambda test event using:

```json
{}
```

### Step 2

Invoked the Lambda function manually.

### Step 3

Verified the Lambda execution result.

Sample Output:

```json
{
  "statusCode": 200,
  "stopped": [
    "i-08c774009764ebc02"
  ],
  "started": [
    "i-0ce2c014f7087f2dd"
  ]
}
```

<img width="2364" height="1344" alt="image" src="https://github.com/user-attachments/assets/f63f3b39-a85d-45b3-8661-dd91794c09c3" />


### Step 4

Verified the EC2 dashboard and confirmed:

* The instance tagged `Auto-Stop` was stopped.
* The instance tagged `Auto-Start` was started.

<img width="2882" height="454" alt="image" src="https://github.com/user-attachments/assets/526608fe-2fdb-4604-9e39-471ed5a9fe44" />

---

## Repository Structure

```text
serverless-ec2-management/
│
├── lambda_function.py
├── README.md
```

---

## Outcome

The AWS Lambda function successfully automated EC2 instance management using Boto3. Based on the instance tags, the function identified the target EC2 instances and performed the required start and stop operations. The assignment demonstrated the practical use of AWS Lambda, IAM roles, EC2 instance tagging, and Boto3 for serverless infrastructure automation.
